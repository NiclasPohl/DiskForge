'''
Function for Changing specified Timestamps (MACE) for a given file in its Metadata
'''

from Utility.SleuthKit.ExtractValuesFromMMLS import mmls_extract_all_partitions, print_partition_list
from Utility.SleuthKit.ExtractValuesFromFLS import extract_values_fls
from Utility.SleuthKit.ExtractValuesFromIstat import istat_extract_inode
from Utility.SleuthKit.ExtractValuesFromFSSTAT import extract_values_fsstat
from Utility.Calculations.OffSetCalculator import calculate_offset_inode
from Utility.FileModification.timestamp_update import timestamp_update, update_inode_checksum
from Utility.Other.WriteTimeModLog import writeTimestampMetaChange, newEntry
import Utility.Checksumming.generate_crc32c as crc32c
import Utility.FileModification.Watermark as Watermark


def Meta_Change(image_location=False, file_location=False, partition_num=False, verbose=False, args=None,timestamp=None, nts=None):
    """
    The Meta_Change function in Python prompts the user for necessary parameters, extracts metadata from
    an image file, modifies timestamps, and updates the checksum of an inode.
    
    :param image_location: The `image_location` parameter is used to specify the location of the image
    file from which you want to extract data, defaults to False (optional)
    :param file_location: The `file_location` parameter in the `Meta_Change` function refers to the
    location of the file whose timestamps you want to modify. If this parameter is not provided when
    calling the function, the user will be prompted to enter the file location, defaults to False
    (optional)

    :param partition_num: The `partition_num` parameter in the `Meta_Change` function is used to specify
    the partition number from which you want to extract metadata. It is an optional parameter that
    allows you to target a specific partition within the image file for metadata modification. If this
    parameter is not provided, the function will, defaults to False (optional)

    :param verbose: The `verbose` parameter in the `Meta_Change` function is used to control whether
    additional information or messages should be displayed during the execution of the function. If
    `verbose` is set to `True`, then extra details or debug information will be printed to the console.
    If `verbose` is, defaults to False (optional)

    :param args: The `args` parameter in the `Meta_Change` function seems to be used to store various
    arguments that are being passed to the function. It is likely a dictionary or an object that holds
    key-value pairs of arguments. In the provided code snippet, it is used to store values for `image

    :param timestamp: The `timestamp` parameter in the `Meta_Change` function is used to specify the
    timestamp you want to modify for a file. This timestamp could be the Accessed timestamp, File
    Modified timestamp, Inode Modified timestamp, File Created timestamp, or all timestamps associated
    with the file. You can provide this

    :param nts: The `nts` parameter in the `Meta_Change` function seems to be used for storing the new
    timestamp that the user wants to set for a file. This parameter allows the user to input the new
    timestamp that should be applied to the file during the metadata change process
    
    :return: The function `Meta_Change` is returning an integer value of 0 if the process completes
    successfully.
    """

    '''
    Check if all needed parameters are given
    If not ask user to supply them
    '''
    if image_location == None:
        image_location = input("Please enter the image file location: ")
        args.image_location = args.image_location
    else:
        image_location = "".join(image_location)
        print(image_location)
    if file_location == None:
        file_location = input("Please enter the location of the file which timestamps you want to modify: ")
        args.file = file_location
    file_location = file_location[0]
    if verbose == None:
        verbose = False

    extracted_partitions = mmls_extract_all_partitions(imagepath=image_location, verbose=verbose)
    if partition_num == None:
        print_partition_list(extracted_partitions)
        partition_num = int(input("\nWhat Partition Number do you want to Extract? "))
        args.partnum = partition_num
    else:
        partition_num = partition_num[0]

    if timestamp == None:
        timestamp = input("Please enter what timestamp you want to modify: ")

    timestamps_to_modify = timestamp

    if nts == None:
        nts = input("Please enter what the new timestamp should be: ")

    newEntry(args)
    partition_to_use = extracted_partitions[partition_num]

    '''
    Extract Inode number of file
    '''
    inode_number = extract_values_fls(imagepath=image_location, offset=str(partition_to_use.start),
                                      searched_file=file_location, verbose=verbose)
    if inode_number == -1:
        print("Error: File not Found")
        return -1

    '''
    Extract the timestamps for the given file
    Then show them user so he can decide on which he wants to modify
    '''
    timestamps_original = istat_extract_inode(imagepath=image_location, offset=str(partition_to_use.start),
                                              inode_number=str(inode_number), verbose=verbose)

    print("\nCurrent Timestamps")
    timestamps_original.print()

    """
    timestamps_to_modify = input(
        "\nWhat Timestamp do you want to modify? (Accessed, File_Modified, Inode_Modified, File_Created, all) ").split(
        " ")
    """

    '''
    Get the metadata and calculate the total offset of the inode
    '''
    file_system_metadata = extract_values_fsstat(imagepath=image_location, offset=str(partition_to_use.start),
                                                 verbose=verbose)

    inode_offset = calculate_offset_inode(inode_num=inode_number, offset_partition=partition_to_use.start,
                                          file_system_metadata=file_system_metadata,
                                          sector_size=partition_to_use.sector_size, verbose=verbose)
    if verbose:
        print("Inode Offset: {}".format(inode_offset))

    '''
    Update the timestamps to the new timestamps
    And show the user the old and new timestamps
    '''
    timestamp_update(timestamps_to_modify, inode_offset, image_location, timestamps_original, verbose=verbose, time=nts)

    crc32c_inode_checksum = crc32c.compute_inode_crc32c(inode_number, partition_to_use.start * int(partition_to_use.sector_size), inode_offset,
                                image_location)
    update_inode_checksum(inode_offset,image_location,crc32c_inode_checksum)

    timestamps_changed = istat_extract_inode(imagepath=image_location, offset=str(partition_to_use.start),
                                             inode_number=str(inode_number), verbose=verbose)

    if verbose:
        print("\nThese are the Original Timestamps:")
        timestamps_original.print()
        print("\nThese are the Modified Timestamps:")
        timestamps_changed.print()

    writeTimestampMetaChange(timestamps_original, timestamps_changed)

    print(inode_offset)

    Watermark.setWaterMark(partition_to_use.start*int(partition_to_use.sector_size),image_location)

    return 0
