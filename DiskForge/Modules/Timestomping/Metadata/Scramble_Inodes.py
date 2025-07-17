from Utility.FileModification import Watermark
from Utility.SleuthKit.ExtractValuesFromMMLS import mmls_extract_all_partitions, print_partition_list
from Utility.SleuthKit.ExtractValuesFromFLS import extract_all_inodes
from Utility.SleuthKit.ExtractValuesFromIstat import istat_extract_inode
from Utility.SleuthKit.ExtractValuesFromFSSTAT import extract_values_fsstat
from Utility.Calculations.OffSetCalculator import calculate_offset_inode
from Utility.Other.WriteTimeModLog import newEntry
from Utility.FileModification.timestamp_update import swap_timestamps
import random


def scramble(image_location=None, partition_num=None, count=None, verbose=None, args=None):
    '''
    Experimental function to scramble the Timestamps of all files on a disk image
    :param image_location: Location of the Disk Image
    :param partition_num: Partition Number
    :param count: How many swaps should happen
    :param verbose: Increase Verbosity
    :return: 0 on success and -1 on failure
    '''

    '''
    Check to see if all parameters are given
    If not ask user
    '''
    if image_location == None:
        image_location = input("Please enter the image file location: ")
        args.image_location = image_location
    else:
        image_location = image_location[0]
    if verbose == None:
        verbose = False

    extracted_partitions = mmls_extract_all_partitions(imagepath=image_location, verbose=verbose)
    if partition_num == None:
        print_partition_list(extracted_partitions)
        partition_num = int(input("\nWhat Partition Number do you want to Extract? "))
        args.partnum = partition_num
    else:
        partition_num = partition_num[0]
    partition_to_use = extracted_partitions[partition_num]

    if count == None:
        count = int(input("\nHow often do you want to swap inode timestamps? "))
        args.count = count

    newEntry(args)
    count = int(count)

    '''
    Extract all the inode numbers of the given partition
    '''
    print("i")
    inode_nums = extract_all_inodes(imagepath=image_location, offset=str(partition_to_use.start))
    fsmeta = extract_values_fsstat(imagepath=image_location, offset=str(partition_to_use.start),
                                   verbose=verbose)
    print("u")
    for i in range(count):
        print(f"{i} von {count}")
        '''
        We use len(inode_nums) and not min and max inode number, because there can be holes/missing numbers in the inode numbers
        '''
        inode_a = random.randrange(len(inode_nums))
        inode_b = random.randrange(len(inode_nums))
        '''
        If inodes match rerun
        '''
        while inode_a == inode_b:
            inode_b = random.randrange(len(inode_nums))
        inode_a = inode_nums[inode_a]
        inode_b = inode_nums[inode_b]

        '''
        Calculate for both inodes the offset
        '''
        file_A_inode_offset = calculate_offset_inode(inode_num=inode_a,
                                                     offset_partition=partition_to_use.start,
                                                     file_system_metadata=fsmeta,
                                                     sector_size=partition_to_use.sector_size, verbose=verbose)
        file_B_inode_offset = calculate_offset_inode(inode_num=inode_b,
                                                     offset_partition=partition_to_use.start,
                                                     file_system_metadata=fsmeta,
                                                     sector_size=partition_to_use.sector_size, verbose=verbose)
        if verbose:
            file_A_ts_orig = istat_extract_inode(imagepath=image_location, offset=str(partition_to_use.start),
                                                 inode_number=str(inode_a), verbose=verbose)
            file_B_ts_orig = istat_extract_inode(imagepath=image_location, offset=str(partition_to_use.start),
                                                 inode_number=str(inode_b), verbose=verbose)
            print("\nInode " + str(inode_a) + " original Timestamps:")
            file_A_ts_orig.print()
            print("\nInode " + str(inode_b) + " original Timestamps:")
            file_B_ts_orig.print()

        '''
        Call the swap functionality for booth inodes
        '''
        swap_timestamps(file_A_inode_offset=file_A_inode_offset, file_B_inode_offset=file_B_inode_offset,
                        image_location=image_location, verbose=verbose)
        if verbose:
            file_A_ts_orig = istat_extract_inode(imagepath=image_location, offset=str(partition_to_use.start),
                                                 inode_number=str(inode_a), verbose=verbose)
            file_B_ts_orig = istat_extract_inode(imagepath=image_location, offset=str(partition_to_use.start),
                                                 inode_number=str(inode_b), verbose=verbose)
            print("\nInode " + str(inode_a) + " new Timestamps:")
            file_A_ts_orig.print()
            print("\nInode " + str(inode_b) + " new Timestamps:")
            file_B_ts_orig.print()

    '''
    Idee:
    Hole Minimale und Maximale Inode Nummer
    Generiere 2 Random Inode Numbers in diesem Bereich
    Rufe Swap mit diesen Beiden Inode Numbers auf
    '''
    Watermark.setWaterMark(partition_to_use.start * int(partition_to_use.sector_size), image_location)
    return 0
