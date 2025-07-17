from Utility.SleuthKit.ExtractValuesFromMMLS import mmls_extract_all_partitions, print_partition_list, print_partition
from Utility.SleuthKit.ExtractValuesFromFLS import extract_values_fls
from Utility.SleuthKit.ExtractValuesFromIstat import istat_extract_inode
from Utility.SleuthKit.ExtractValuesFromFSSTAT import extract_values_fsstat
from Utility.Calculations.OffSetCalculator import calculate_offset_inode
from Utility.FileModification.timestamp_update import timestamp_update

# TODO add verbose Setting
verbose = False

# Could throw exception ValueError: too many values to unpack (expected 2)
image_location, file_location = input(
    "Please enter the Disk Image Location and the Location of the File you want to modify: ").split(" ")

# Just for Testing Purposes TODO remove
image_location = "/home/niclas/Utility.img"
file_location = "TestFile1"

extracted_partitions = mmls_extract_all_partitions(imagepath=image_location, verbose=verbose)
print_partition_list(extracted_partitions)

part_num = int(input("\nWhat Partition Number do you want to Extract? "))

partition_to_use = extracted_partitions[part_num]
if verbose:
    print_partition(partition=partition_to_use)

# TODO Error Handling
inode_number = extract_values_fls(imagepath=image_location, offset=str(partition_to_use.start),
                                  searched_file=file_location, verbose=verbose)

timestamps_original = istat_extract_inode(imagepath=image_location, offset=str(partition_to_use.start),
                                          inode_number=str(inode_number), verbose=verbose)

print("\nCurrent Timestamps")
timestamps_original.print()

timestamps_to_modify = input(
    "\nWhat Timestamp do you want to modify? (Accessed, File_Modified, Inode_Modified, File_Created) ").split(" ")

file_system_metadata = extract_values_fsstat(imagepath=image_location, offset=str(partition_to_use.start),
                                             verbose=verbose)
if verbose:
    file_system_metadata.print()

inode_offset = calculate_offset_inode(inode_num=inode_number, offset_partition=partition_to_use.start,
                                      file_system_metadata=file_system_metadata,
                                      sector_size=partition_to_use.sector_size, verbose=verbose)
if verbose:
    print("\n Inode Offset is: " + str(inode_offset))

timestamp_update(timestamps_to_modify, inode_offset, image_location, timestamps_original, verbose=verbose)

timestamps_changed = istat_extract_inode(imagepath=image_location, offset=str(partition_to_use.start),
                                         inode_number=str(inode_number), verbose=verbose)

print("\nThese are the Original Timestamps:")
timestamps_original.print()
print("\nThese are the Modified Timestamps:")
timestamps_changed.print()
