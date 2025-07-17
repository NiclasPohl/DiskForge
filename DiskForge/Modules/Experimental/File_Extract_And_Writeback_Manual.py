from Utility.SleuthKit.ExtractValuesFromFLS import extract_values_fls
from Utility.SleuthKit.ExtractValuesFromMMLS import mmls_extract_all_partitions, print_partition_list
from Utility.FileModification.WriteByteToImageFileData import writeback
from Utility.Other.WriteTimeModLog import writeStderr, newEntry
import Utility.Other.Terminal_Commands as command


def extractFile(image_location=None, files=None,
                partition_num=None, verbose=None, args=None):
    if image_location == None:
        image_location = input("Please enter the image file location: ")
        args.image_location = image_location
    else:
        image_location = image_location[0]

    if files == None:
        file_location_on_disk_image = input("Please enter the location of the file on the disk image: ")
        file_location_on_user_pc = input("Please enter the location of the file on your pc: ")
    elif len(files) == 1:
        file_location_on_disk_image = files[0]
        file_location_on_user_pc = input("Please enter the location of the file on your pc: ")
    else:
        file_location_on_disk_image = files[0]
        file_location_on_user_pc = files[1]

    if file_location_on_disk_image == None:
        file_location_on_disk_image = input("Please enter the location of the file on the disk image: ")
    else:
        file_location_on_disk_image = file_location_on_disk_image[0]
    if file_location_on_user_pc == None:
        file_location_on_user_pc = input("Please enter the location of the file on your pc: ")
    else:
        file_location_on_user_pc = file_location_on_disk_image[0]
    args.file = ' '.join([file_location_on_disk_image, file_location_on_user_pc])
    extracted_partitions = mmls_extract_all_partitions(imagepath=image_location, verbose=verbose)
    if partition_num == None:
        print_partition_list(extracted_partitions)
        partition_num = int(input("\nWhat Partition Number do you want to Extract? "))
        args.partnum = partition_num
    else:
        partition_num = partition_num[0]
    newEntry(args)
    partition_to_use = extracted_partitions[partition_num]
    inode_number = extract_values_fls(imagepath=image_location, offset=str(partition_to_use.start),
                                      searched_file=file_location_on_disk_image, verbose=verbose)
    if (inode_number == -1):
        print("Failure to find file")
        writeStderr("Failure to find file")
        return -1

    command.icat(partition_to_use.start, image_location, inode_number, file_location_on_user_pc)

    return 0


def writebackFile(image_location=None, files=None,
                  partition_num=None, verbose=None, update=False, args=None):
    if image_location == None:
        image_location = input("Please enter the image file location: ")
        args.image_location = image_location
    else:
        image_location = image_location[0]

    if files == None:
        file_location_on_disk_image = input("Please enter the location of the file on the disk image: ")
        file_location_on_user_pc = input("Please enter the location of the file on your pc: ")
    elif len(files) == 1:
        file_location_on_disk_image = files[0]
        file_location_on_user_pc = input("Please enter the location of the file on your pc: ")
    else:
        file_location_on_disk_image = files[0]
        file_location_on_user_pc = files[1]
    args.file = ' '.join([file_location_on_disk_image, file_location_on_user_pc])
    extracted_partitions = mmls_extract_all_partitions(imagepath=image_location, verbose=verbose)
    if partition_num == None:
        print_partition_list(extracted_partitions)
        partition_num = int(input("\nWhat Partition Number do you want to Extract? "))
        args.partnum = partition_num
    else:
        partition_num = partition_num[0]
    newEntry(args)
    partition_to_use = extracted_partitions[partition_num]
    inode_number = extract_values_fls(imagepath=image_location, offset=str(partition_to_use.start),
                                      searched_file=file_location_on_disk_image, verbose=verbose)
    if (inode_number == -1):
        print("Failure to find file")
        writeStderr("Failure to find file")
        return -1

    writeback(image_location=image_location, partition_to_use=partition_to_use, inode_number=inode_number,
              file_path=file_location_on_user_pc, verbose=verbose, update=update)
    return None
