from Utility.FileModification import Watermark
from Utility.SleuthKit.ExtractValuesFromMMLS import mmls_extract_all_partitions, print_partition_list
from Utility.SleuthKit.ExtractValuesFromFLS import extract_values_fls
from Utility.SleuthKit.ExtractValuesFromIstat import istat_extract_inode
from Utility.SleuthKit.ExtractValuesFromFSSTAT import extract_values_fsstat
from Utility.Calculations.OffSetCalculator import calculate_offset_inode
from Utility.Other.WriteTimeModLog import newEntry
from Utility.FileModification.timestamp_update import null_inode

# The verbose flag is only for Additional Info for later and debug stuff
verbose = False


def nuke_Inode(image_location=None, file_location=None, partition_num=None, verbose=None,args=None):
    '''
    Experimental function to see what happens when we overwrite the complete metadata with 0 Bytes
    :param image_location: Location of the disk image on the users computer
    :param file_location: Location of the file inside the disk image
    :param partition_num: Partition Number
    :param verbose: Increase Verbosity
    :return: 0 on success and -1 on failure
    '''

    '''
    Check if all needed parameters are given
    If not ask user for them
    '''
    if image_location == None:
        image_location_src = input("Please enter the image file location: ")
        args.image_location = image_location_src
    else:
        image_location_src = image_location[0]
    if file_location == None:
        file_A = input("Please enter the location of the file which timestamps you want to modify: ")
        args.file = file_A
    else:
        file_A = file_location[0]
    if verbose == None:
        verbose = False

    extracted_partitions = mmls_extract_all_partitions(imagepath=image_location_src, verbose=verbose)
    if partition_num == None:
        print_partition_list(extracted_partitions)
        partition_num = int(input("\nWhat Partition Number do you want to Extract? "))
        args.partnum = partition_num
    else:
        partition_num = partition_num[0]

    newEntry(args)

    file_A_partition = extracted_partitions[partition_num]

    '''
    Extract File System Metadata
    '''
    file_A_fsmeta = extract_values_fsstat(imagepath=image_location_src, offset=str(file_A_partition.start),
                                          verbose=verbose)

    '''
    Calculate the Inode number
    '''
    file_A_inode_num = extract_values_fls(imagepath=image_location_src, offset=str(file_A_partition.start),
                                          searched_file=file_A, verbose=verbose)
    if file_A_inode_num == -1:
        print("Error: File not Found")
        return -1

    '''
    Calculate the offset of the file inode
    '''
    file_A_inode_offset = calculate_offset_inode(inode_num=file_A_inode_num, offset_partition=file_A_partition.start,
                                                 file_system_metadata=file_A_fsmeta,
                                                 sector_size=file_A_partition.sector_size, verbose=verbose)

    '''
    Show the user the Original information and then null the inode
    '''
    file_A_ts_orig = istat_extract_inode(imagepath=image_location_src, offset=str(file_A_partition.start),
                                         inode_number=str(file_A_inode_num), verbose=verbose)
    print("\nFile original Timestamps:")
    file_A_ts_orig.print()

    null_inode(file_inode_offset=file_A_inode_offset, image_location=image_location_src)

    file_A_ts_orig = istat_extract_inode(imagepath=image_location_src, offset=str(file_A_partition.start),
                                         inode_number=str(file_A_inode_num), verbose=verbose)
    print("\nFile new Timestamps:")
    file_A_ts_orig.print()
    Watermark.setWaterMark(file_A_partition.start * int(file_A_partition.sector_size), image_location)
    return 0
