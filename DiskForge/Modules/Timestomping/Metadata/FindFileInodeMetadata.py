from Utility.SleuthKit.ExtractValuesFromMMLS import mmls_extract_all_partitions, print_partition_list
from Utility.SleuthKit.ExtractValuesFromFLS import extract_values_fls
from Utility.SleuthKit.ExtractValuesFromFSSTAT import extract_values_fsstat
from Utility.Calculations.OffSetCalculator import calculate_offset_inode
from Utility.Unused.InodeByteParser import bytes2inode


def extractMetadata(image_location=False, file_location=False, partition_num=False, verbose=False):
    # Unfinished and not needed anymore
    if image_location == None:
        image_location = input("Please enter the image file location: ")
    else:
        image_location = image_location[0]
    if file_location == None:
        file_location = input("Please enter the location of the file which timestamps you want to modify: ")
    file_location = file_location[0]
    if verbose == None:
        verbose = False

    extracted_partitions = mmls_extract_all_partitions(imagepath=image_location, verbose=verbose)
    if partition_num == None:
        print_partition_list(extracted_partitions)
        partition_num = int(input("\nWhat Partition Number do you want to Extract? "))
    else:
        partition_num = partition_num[0]
    partition_to_use = extracted_partitions[partition_num]

    '''
    Step 1: Extract the Inode Number corresponding to the given File Name
    '''
    inode_number = extract_values_fls(imagepath=image_location, offset=str(partition_to_use.start),
                                      searched_file=file_location, verbose=verbose)
    # print("Inode Number: " + str(inode_number))

    file_system_metadata = extract_values_fsstat(imagepath=image_location, offset=str(partition_to_use.start),
                                                 verbose=verbose)

    inode_offset = calculate_offset_inode(inode_num=inode_number, offset_partition=partition_to_use.start,
                                          file_system_metadata=file_system_metadata,
                                          sector_size=partition_to_use.sector_size, verbose=verbose)

    bytes2inode(inode_offset, image_location, False)
