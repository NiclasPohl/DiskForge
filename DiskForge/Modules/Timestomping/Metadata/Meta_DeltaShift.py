from Utility.FileModification import Watermark
from Utility.SleuthKit.ExtractValuesFromMMLS import mmls_extract_all_partitions, print_partition_list
from Utility.SleuthKit.ExtractValuesFromFLS import extract_values_fls
from Utility.SleuthKit.ExtractValuesFromIstat import istat_extract_inode
from Utility.SleuthKit.ExtractValuesFromFSSTAT import extract_values_fsstat
from Utility.Calculations.OffSetCalculator import calculate_offset_inode
from Utility.Other.WriteTimeModLog import newEntry
from Utility.FileModification.timestamp_update import timestamp_shift, update_inode_checksum
import Utility.Checksumming.generate_crc32c as crc32c


def Meta_DeltaShift(image_location=False, file_location=None, partition_num=False, shift_type=None, shift_num=None,verbose=False, args=None, timestamp=None):
    """
    The Meta_DeltaShift function modifies timestamps in a disk image file based on user input for shift
    type and amount.
    
    :param image_location: The `image_location` parameter in the `Meta_DeltaShift` function is used to
    specify the location of the image file. This image file is typically a disk image from which
    partitions and file system information will be extracted for timestamp modification. If the
    `image_location` parameter is not provided when calling, defaults to False (optional)
    :param file_location: The `file_location` parameter in the `Meta_DeltaShift` function is used to
    specify the location of the file whose timestamps you want to modify. If the `file_location`
    parameter is not provided when calling the function, it will prompt the user to enter the file
    location
    :param partition_num: The `partition_num` parameter in the `Meta_DeltaShift` function is used to
    specify the partition number from which you want to extract data. It allows you to choose a specific
    partition from the list of extracted partitions to perform operations on. If the `partition_num` is
    not provided as an, defaults to False (optional)
    :param shift_type: The `shift_type` parameter in the `Meta_DeltaShift` function is used to specify
    the type of shift you want to perform on the timestamps. It can take values such as "second",
    "minute", "hour", or "day" to indicate the unit of time by which you want
    :param shift_num: The `shift_num` parameter in the `Meta_DeltaShift` function represents the number
    by which you want to shift the timestamps. It is an integer value that determines the amount of
    shift to be applied to the timestamps in the specified units (seconds, minutes, hours, or days).
    This value
    :param verbose: The `verbose` parameter in the `Meta_DeltaShift` function is used to control whether
    additional information or messages should be displayed during the execution of the function. If
    `verbose` is set to `True`, more detailed information will be printed out, aiding in debugging or
    understanding the process. If, defaults to False (optional)
    :param args: The `args` parameter in the `Meta_DeltaShift` function seems to be a dictionary-like
    object that is used to store and pass various arguments and values throughout the function. It
    appears to be used to keep track of values such as `image_location`, `file_location`,
    `partition_num`,
    """
    shift_multiplicator = 1
    if image_location == None:
        image_location = input("Please enter the image file location: ")
        args.image_location = image_location
    else:
        image_location = image_location[0]
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
        timestamp = input(
        "\nWhat Timestamp do you want to modify? (Accessed, File_Modified, Inode_Modified, File_Created, all) ").split(
        " ")

    timestamps_to_modify = timestamp

    partition_to_use = extracted_partitions[partition_num]

    '''
    Specify the amount of seconds needed to be shiftet
    Internally we work on seconds
    '''
    if shift_type == None:
        shift_type = input("Please enter what type of shift you want to do (second, minute, hour, day): ")
        args.shift_type = shift_type
    match shift_type:
        case "second":
            shift_multiplicator = 1
        case "minute":
            shift_multiplicator = 60
        case "hour":
            shift_multiplicator = 60 * 60
        case "day":
            shift_multiplicator = 60 * 60 * 24

    if shift_num == None:
        shift_num = int(input("Please enter the number you want to shift by: "))
        args.shift_num = shift_num
    else:
        shift_num = int(shift_num)

    newEntry(args)

    '''
    Extract Inode Number
    '''
    inode_number = extract_values_fls(imagepath=image_location, offset=str(partition_to_use.start),
                                      searched_file=file_location, verbose=verbose)

    if (inode_number == -1):
        print("Error: File not Found")
        return -1

    timestamps_original = istat_extract_inode(imagepath=image_location, offset=str(partition_to_use.start),
                                              inode_number=str(inode_number), verbose=verbose)
    '''
    Display current timestamps and ask user which he wants to modify
    '''
    print("\nCurrent Timestamps")
    timestamps_original.print()


    '''
    Calculate the total offset of the inode
    '''
    file_system_metadata = extract_values_fsstat(imagepath=image_location, offset=str(partition_to_use.start),
                                                 verbose=verbose)

    inode_offset = calculate_offset_inode(inode_num=inode_number, offset_partition=partition_to_use.start,
                                          file_system_metadata=file_system_metadata,
                                          sector_size=partition_to_use.sector_size, verbose=verbose)

    '''
    Shift the timestamp and print original and changed timestamps
    '''
    timestamp_shift(timestamps_to_modify, inode_offset, image_location, timestamps_original,
                    shift_num * shift_multiplicator, verbose=verbose)
    crc32c_inode_checksum = crc32c.compute_inode_crc32c(inode_number, partition_to_use.start * int(partition_to_use.sector_size), inode_offset,
                                image_location)
    update_inode_checksum(inode_offset,image_location,crc32c_inode_checksum)

    timestamps_changed = istat_extract_inode(imagepath=image_location, offset=str(partition_to_use.start),
                                             inode_number=str(inode_number), verbose=verbose)

    print("\nThese are the Original Timestamps:")
    timestamps_original.print()
    print("\nThese are the Modified Timestamps:")
    timestamps_changed.print()

    Watermark.setWaterMark(partition_to_use.start * int(partition_to_use.sector_size), image_location)

    return 0
