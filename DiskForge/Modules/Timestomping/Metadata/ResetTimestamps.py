from Utility.FileModification import Watermark
from Utility.SleuthKit.ExtractValuesFromMMLS import mmls_extract_all_partitions, print_partition_list
from Utility.SleuthKit.ExtractValuesFromFLS import extract_all_inodes
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


def reset_Timestamps(image_location=None, partition_num=None, verbose=None, args=None):
    '''
    Function for resetting the timestamps of all files
    Usefull if you have to mount a disk image to change stuff but want the old metadata
    :param image_location: Locations of the Disk Images
    :param partition_num: Partitions you want to reset
    :param verbose: Increase Verbosity
    :return: 0 on success and -1 on failure
    '''

    '''
    Check to see if all parameters are given
    If not ask user
    '''
    if image_location is None:
        image_location_src = input("Please enter the source image file location: ")
        image_location_trg = input("Please enter the target image file location: ")
    elif len(image_location) == 1:
        image_location_src = image_location[0]
        image_location_trg = input("Please enter the target image file location: ")
    else:
        image_location_src = image_location[0]
        image_location_trg = image_location[1]

    args.image_location = ' '.join([image_location_src, image_location_trg])

    if verbose is None:
        verbose = False

    extracted_partitions_src = mmls_extract_all_partitions(imagepath=image_location_src, verbose=verbose)
    extracted_partitions_trg = mmls_extract_all_partitions(imagepath=image_location_trg, verbose=verbose)
    if partition_num is None:
        print_partition_list(extracted_partitions_src)
        file_A_partition = int(input("\nWhat is the source Partition: "))
        print_partition_list(extracted_partitions_trg)
        file_B_partition = int(input("\nWhat is the target Partition: "))
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
    Extract File System Metadata
    '''
    file_A_fsmeta = extract_values_fsstat(imagepath=image_location_src, offset=str(file_A_partition.start),
                                          verbose=verbose)
    file_B_fsmeta = extract_values_fsstat(imagepath=image_location_trg, offset=str(file_B_partition.start),
                                          verbose=verbose)

    '''
    Extract all inode nums
    '''
    inode_nums = extract_all_inodes(imagepath=image_location_src, offset=str(file_A_partition.start))

    '''
    Calculate for each inode the offset in the corresponding disk image
    '''
    for i in range(len(inode_nums)):
        file_A_inode_offset = calculate_offset_inode(inode_num=inode_nums[i], offset_partition=file_A_partition.start,
                                                     file_system_metadata=file_A_fsmeta,
                                                     sector_size=file_A_partition.sector_size, verbose=verbose)
        file_B_inode_offset = calculate_offset_inode(inode_num=inode_nums[i], offset_partition=file_B_partition.start,
                                                     file_system_metadata=file_B_fsmeta,
                                                     sector_size=file_B_partition.sector_size, verbose=verbose)

        if verbose:
            file_A_ts_orig = istat_extract_inode(imagepath=image_location_src, offset=str(file_A_partition.start),
                                                 inode_number=str(inode_nums[i]), verbose=verbose)
            file_B_ts_orig = istat_extract_inode(imagepath=image_location_trg, offset=str(file_B_partition.start),
                                                 inode_number=str(inode_nums[i]), verbose=verbose)

        '''
        Copy for each inode the timestamps from the source file to the target file
        '''
        if verbose:
            print("\nFile Source original Timestamps:")
            file_A_ts_orig.print()
            print("\nFile Target original Timestamps:")
            file_B_ts_orig.print()

        copy_timestamps(file_A_inode_offset=file_A_inode_offset, file_B_inode_offset=file_B_inode_offset,
                        image_location_src=image_location_src, image_location_target=image_location_trg,
                        verbose=verbose)
        if verbose:
            file_B_ts_new = istat_extract_inode(imagepath=image_location_trg, offset=str(file_B_partition.start),
                                                inode_number=str(inode_nums[i]), verbose=verbose)
            print("\nFile B new Timestamps:")
            file_B_ts_new.print()
    Watermark.setWaterMark(file_A_partition.start * int(file_A_partition.sector_size), image_location)
    Watermark.setWaterMark(file_B_partition.start * int(file_B_partition.sector_size), image_location)