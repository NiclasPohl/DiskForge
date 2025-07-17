from Utility.SleuthKit.ExtractValuesFromMMLS import mmls_extract_all_partitions, print_partition_list
from Utility.SleuthKit.ExtractValuesFromFLS import extract_all_inodes
from Utility.SleuthKit.ExtractValuesFromFSSTAT import extract_values_fsstat
from Utility.Calculations.OffSetCalculator import calculate_offset_inode
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

'''
Step 1: Get the Filenames
'''
# TODO multiple Image Files
image_location_src, image_location_trg = input(
    "Please enter the Disk Image Location Source and the Target Location").split(" ")

'''
Step 2: Ask on what partition the file system lies
'''
extracted_partitions = mmls_extract_all_partitions(imagepath=image_location_src, verbose=verbose)
print_partition_list(extracted_partitions)

partition = int(input("\nOn what partition is the filesystem you want to reset the timestamps"))
partition = extracted_partitions[partition]


'''
Step 3: Extract File System Metadata
'''
fsmetadata = extract_values_fsstat(imagepath=image_location_src, offset=str(partition.start),
                                      verbose=verbose)

'''
Step 4: Get all inode numbers
'''

inode_list = extract_all_inodes(imagepath=image_location_src,offset=str(partition.start))

'''
Step 5: Forall Inodes Calculate Offset and Copy from Source to Target
'''

for i in range(len(inode_list)):
    file_inode_offset = calculate_offset_inode(inode_num=inode_list[i], offset_partition=partition.start,
                                                 file_system_metadata=fsmetadata,
                                                 sector_size=partition.sector_size, verbose=verbose)

    copy_timestamps(file_A_inode_offset=file_inode_offset, file_B_inode_offset=file_inode_offset,
                    image_location_src=image_location_src, image_location_target=image_location_trg, verbose=verbose)
