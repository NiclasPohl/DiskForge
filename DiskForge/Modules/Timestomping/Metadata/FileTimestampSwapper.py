from Utility.FileModification import Watermark
from Utility.SleuthKit.ExtractValuesFromMMLS import mmls_extract_all_partitions, print_partition_list
from Utility.SleuthKit.ExtractValuesFromFLS import extract_values_fls
from Utility.SleuthKit.ExtractValuesFromIstat import istat_extract_inode
from Utility.SleuthKit.ExtractValuesFromFSSTAT import extract_values_fsstat
from Utility.Calculations.OffSetCalculator import calculate_offset_inode
from Utility.FileModification.timestamp_update import swap_timestamps
from Utility.Other.WriteTimeModLog import swappedMetadata, newEntry

# The verbose flag is only for Additional Info for later and debug stuff
verbose = False

'''
Idea:
We ask the user for two files A and B.
We than take the timestamp metadata from A and B and save it.
Now we just need to write it to the locations
Need to modify the methods so we can give stuff via parameter
'''


def swap_Timestamps(image_location=None, file_location=None, partition_num=None, verbose=None, args=None):
    '''
    Function for swapping the timestamps of two files
    :param image_location: Location of the disk image
    :param file_location: Location of the files inside the disk image
    :param partition_num: Partition Number
    :param verbose: Increase Verbosity
    :return: 0 on success and -1 on failure
    '''

    '''
    Check if all needed parameters are given
    If not ask user to supply them
    '''
    if image_location == None:
        image_location = input("Please enter the image file location: ")
        args.image_location = image_location
    else:
        image_location = image_location[0]
    if file_location == None:
        file_A = input("Please enter the location of the source file: ")
        file_B = input("Please enter the location of the target file: ")
    elif len(file_location) == 1:
        file_A = file_location[0]
        file_B = input("Please enter the location of the target file: ")
    else:
        file_A = file_location[0]
        file_B = file_location[1]
    args.file = ' '.join([file_A, file_B])
    if verbose == None:
        verbose = False

    extracted_partitions = mmls_extract_all_partitions(imagepath=image_location, verbose=verbose)
    if partition_num == None:
        print_partition_list(extracted_partitions)
        file_A_partition = int(input("\nOn what Partition is the file A: "))
        file_B_partition = int(input("\nOn what Partition is the file B: "))
    elif len(partition_num) == 1:
        file_A_partition = partition_num[0]
        file_B_partition = partition_num[0]
    else:
        file_A_partition = partition_num[0]
        file_B_partition = partition_num[1]
    args.partnum = ' '.join([file_A_partition, file_B_partition])
    file_A_partition = extracted_partitions[file_A_partition]
    file_B_partition = extracted_partitions[file_B_partition]

    newEntry(args)
    '''
    Extract File System Metadata
    '''
    file_A_fsmeta = extract_values_fsstat(imagepath=image_location, offset=str(file_A_partition.start),
                                          verbose=verbose)
    file_B_fsmeta = extract_values_fsstat(imagepath=image_location, offset=str(file_B_partition.start),
                                          verbose=verbose)

    '''
    Calculate Inode Numbers
    '''
    file_A_inode_num = extract_values_fls(imagepath=image_location, offset=str(file_A_partition.start),
                                          searched_file=file_A, verbose=verbose)
    file_B_inode_num = extract_values_fls(imagepath=image_location, offset=str(file_B_partition.start),
                                          searched_file=file_B, verbose=verbose)

    '''
    Calculate Inode Offset 
    '''
    file_A_inode_offset = calculate_offset_inode(inode_num=file_A_inode_num, offset_partition=file_A_partition.start,
                                                 file_system_metadata=file_A_fsmeta,
                                                 sector_size=file_A_partition.sector_size, verbose=verbose)
    file_B_inode_offset = calculate_offset_inode(inode_num=file_B_inode_num, offset_partition=file_B_partition.start,
                                                 file_system_metadata=file_B_fsmeta,
                                                 sector_size=file_B_partition.sector_size, verbose=verbose)

    if (file_A_inode_num == -1):
        print("Error: Source File not found")
        return -1
    if (file_B_inode_num == -1):
        print("Error: Target File not found")
        return -1

    '''
    Save original Metadata and then Swap the timestamps
    '''
    file_A_ts_orig = istat_extract_inode(imagepath=image_location, offset=str(file_A_partition.start),
                                         inode_number=str(file_A_inode_num), verbose=verbose)
    file_B_ts_orig = istat_extract_inode(imagepath=image_location, offset=str(file_B_partition.start),
                                         inode_number=str(file_B_inode_num), verbose=verbose)

    swappedMetadata((file_A_inode_num, file_A_inode_offset, file_B_inode_num, file_B_inode_offset))

    '''
    Print old and new timestamps
    '''
    print("\nFile A original Timestamps:")
    file_A_ts_orig.print()
    print("File B original Timestamps:")
    file_B_ts_orig.print()
    swap_timestamps(file_A_inode_offset=file_A_inode_offset, file_B_inode_offset=file_B_inode_offset,
                    image_location=image_location, verbose=verbose)
    file_A_ts_new = istat_extract_inode(imagepath=image_location, offset=str(file_A_partition.start),
                                        inode_number=str(file_A_inode_num), verbose=verbose)
    file_B_ts_new = istat_extract_inode(imagepath=image_location, offset=str(file_B_partition.start),
                                        inode_number=str(file_B_inode_num), verbose=verbose)

    print("\nFile A new Timestamps:")
    file_A_ts_new.print()
    print("File B new Timestamps:")
    file_B_ts_new.print()
    Watermark.setWaterMark(file_A_partition.start * int(file_A_partition.sector_size), image_location)
    Watermark.setWaterMark(file_B_partition.start * int(file_B_partition.sector_size), image_location)
    return 0
