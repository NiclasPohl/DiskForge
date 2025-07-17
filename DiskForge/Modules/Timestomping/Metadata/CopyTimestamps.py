from Utility.FileModification import Watermark
from Utility.SleuthKit.ExtractValuesFromMMLS import mmls_extract_all_partitions, print_partition_list
from Utility.SleuthKit.ExtractValuesFromFLS import extract_values_fls
from Utility.SleuthKit.ExtractValuesFromIstat import istat_extract_inode
from Utility.SleuthKit.ExtractValuesFromFSSTAT import extract_values_fsstat
from Utility.Calculations.OffSetCalculator import calculate_offset_inode
from Utility.Other.WriteTimeModLog import newEntry
from Utility.FileModification.timestamp_update import copy_timestamps

# The verbose flag is only for Additional Info for later and debug stuff
verbose = False

'''
Idea:
We ask the user for two files A and B.
We than take the timestamp metadata from A and B and save it.
Now we just need to write it to the locations
Need to modify the methods so we can give stuff via parameter
'''


def copy_Timestamps(image_location=None, file_location=None, partition_num=None, verbose=None, args=None):
    '''
    Method for Copying the Timestamps of the file metadata from one file to another
    :param image_location: The one or two images
    :param file_location: The locations of the file
    :param partition_num: The partition numbers of the files
    :param verbose: Increase Verbosity
    :return: 0 on success and -1 on error
    '''

    '''
    Check if all needed parameters are given
    If not ask user to supply them
    '''
    if image_location == None:
        image_location_src = input("Please enter the source image file location: ")
        image_location_trg = input("Please enter the target image file location: ")
    elif len(image_location) == 1:
        image_location_src = image_location[0]
        image_location_trg = image_location[0]
    else:
        image_location_src = image_location[0]
        image_location_trg = image_location[1]

    args.image_location = ' '.join([image_location_src, image_location_trg])

    if file_location == None:
        file_A = input("Please enter the location of the source file: ")
        file_B = input("Please enter the location of the target file: ")
    if len(file_location) == 1:
        file_A = file_location[0]
        file_B = file_location[0]
    else:
        file_A = file_location[0]
        file_B = file_location[1]
    args.file = ' '.join([file_A, file_B])

    if verbose == None:
        verbose = False

    extracted_partitions_src = mmls_extract_all_partitions(imagepath=image_location_src, verbose=verbose)
    extracted_partitions_trg = mmls_extract_all_partitions(imagepath=image_location_trg, verbose=verbose)
    if partition_num == None:
        print_partition_list(extracted_partitions_src)
        file_A_partition = int(input("\nOn what Partition is the source file: "))
        print_partition_list(extracted_partitions_trg)
        file_B_partition = int(input("\nOn what Partition is the target file: "))
    elif len(partition_num) == 1:
        file_A_partition = partition_num[0]
        file_B_partition = partition_num[0]
    else:
        file_A_partition = partition_num[0]
        file_B_partition = partition_num[1]

    args.partnum = ' '.join([file_A_partition, file_B_partition])

    newEntry(args)

    file_A_partition = extracted_partitions_src[file_A_partition]
    file_B_partition = extracted_partitions_trg[file_B_partition]

    '''
    Extract Metadata for the files
    '''
    file_A_fsmeta = extract_values_fsstat(imagepath=image_location_src, offset=str(file_A_partition.start),
                                          verbose=verbose)
    file_B_fsmeta = extract_values_fsstat(imagepath=image_location_trg, offset=str(file_B_partition.start),
                                          verbose=verbose)

    '''
    Calculate Inode Numbers
    '''
    file_A_inode_num = extract_values_fls(imagepath=image_location_src, offset=str(file_A_partition.start),
                                          searched_file=file_A, verbose=verbose)
    file_b_inode_num = extract_values_fls(imagepath=image_location_trg, offset=str(file_B_partition.start),
                                          searched_file=file_B, verbose=verbose)

    if (file_A_inode_num == -1):
        print("Error: Source File not found")
        return -1
    if (file_b_inode_num == -1):
        print("Error: Target File not found")
        return -1

    '''
    Calculate Inode offset
    '''
    file_A_inode_offset = calculate_offset_inode(inode_num=file_A_inode_num, offset_partition=file_A_partition.start,
                                                 file_system_metadata=file_A_fsmeta,
                                                 sector_size=file_A_partition.sector_size, verbose=verbose)
    file_B_inode_offset = calculate_offset_inode(inode_num=file_b_inode_num, offset_partition=file_B_partition.start,
                                                 file_system_metadata=file_B_fsmeta,
                                                 sector_size=file_B_partition.sector_size, verbose=verbose)

    '''
    Get original timestamps
    '''
    file_A_ts_orig = istat_extract_inode(imagepath=image_location_src, offset=str(file_A_partition.start),
                                         inode_number=str(file_A_inode_num), verbose=verbose)
    file_B_ts_orig = istat_extract_inode(imagepath=image_location_trg, offset=str(file_B_partition.start),
                                         inode_number=str(file_b_inode_num), verbose=verbose)

    '''
    Copy timestamps from source to target
    '''
    print("\nFile Source original Timestamps:")
    file_A_ts_orig.print()
    print("File Target original Timestamps:")
    file_B_ts_orig.print()

    copy_timestamps(file_A_inode_offset=file_A_inode_offset, file_B_inode_offset=file_B_inode_offset,
                    image_location_src=image_location_src, image_location_target=image_location_trg, verbose=verbose)

    file_B_ts_new = istat_extract_inode(imagepath=image_location_trg, offset=str(file_B_partition.start),
                                        inode_number=str(file_b_inode_num), verbose=verbose)

    print("\nFile B new Timestamps:")
    file_B_ts_new.print()
    Watermark.setWaterMark(file_A_partition.start * int(file_A_partition.sector_size), image_location)
    Watermark.setWaterMark(file_B_partition.start * int(file_B_partition.sector_size), image_location)
    return 0
