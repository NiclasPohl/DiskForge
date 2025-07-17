import mmap

from Utility.File_Operations.ExtractBytesFromHexFile import extractBytesFromHex
from Utility.Calculations.OffSetCalculator import calculate_offset_block, calculate_offset_inode
import Utility.Other.Terminal_Commands as commando
from Utility.SleuthKit.ExtractValuesFromFSSTAT import extract_values_fsstat
from Utility.SleuthKit.ExtractValuesFromIstat import istat_extract_inode
import Utility.Other.Terminal_Commands as command
from Utility.Other.WriteTimeModLog import file_to_large
from Utility.FileModification.timestamp_update import modifyFileLength


def get_pagesize():
    '''
    Gets the pagesize from the system.
    This is important for the mmap module to work correctly
    :return: Returns the int value of the Page Size
    '''
    result = commando.getconf("PAGE_SIZE")
    result = int(result.stdout)
    return result


def writeback(image_location, partition_to_use, inode_number, file_path, verbose, update):
    """
    The function `writeback` performs various operations related to updating inode data and file
    contents in a file system image.
    
    :param image_location: The `image_location` parameter refers to the location of the image file you
    are working with. This could be the path to a disk image or a similar file that contains the
    filesystem you are analyzing or modifying
    :param partition_to_use: The `partition_to_use` parameter in the `writeback` function is used to
    specify the partition on which the file system metadata and inode data are located. It contains
    information such as the start offset of the partition and the sector size of the partition. This
    information is crucial for extracting and modifying data
    :param inode_number: The `inode_number` parameter in the `writeback` function represents the unique
    identifier of an inode in a file system. The inode contains metadata about a specific file or
    directory, such as permissions, timestamps, and pointers to data blocks
    :param file_path: The `file_path` parameter in the `writeback` function is the path to the file that
    will be hexdumped and its bytes will be extracted for comparison with the inode data
    :param verbose: The `verbose` parameter in the `writeback` function is used to control whether
    additional information and messages should be printed during the execution of the function. If
    `verbose` is set to `True`, the function will print out various messages to provide more details
    about the process. If `verbose`
    :param update: The `update` parameter in the `writeback` function is a boolean flag that determines
    whether to update the Inode Length Field or not. If `update` is set to `True`, the function will
    proceed with updating the Inode Length Field. If `update` is set to `False
    :return: The function `writeback` is returning the integer value `0`.
    """
    file_system_metadata = extract_values_fsstat(imagepath=image_location, offset=str(partition_to_use.start),
                                                 verbose=verbose)
    inode_data = istat_extract_inode(imagepath=image_location, inode_number=inode_number,
                                     offset=str(partition_to_use.start), verbose=verbose)
    command.hexdump(file_path, "newfile")
    bytes = extractBytesFromHex("./newfile", verbose=verbose)
    if (inode_data.size == len(bytes)):
        if (verbose):
            print("Inode Data Size and File Size Match")
            print("Inode Data Size: {}\n".format(inode_data.size))
    elif (inode_data.size < len(bytes)):
        print("Inode Data Size is smaller than File Size by {} Bytes".format(len(bytes) - inode_data.size))
        print("Inode Values should be updated")
        print("Check if whole data fits into the direct blocks\n")
    else:
        if verbose:
            print("Inode Data Size is bigger than File Size by {} Bytes".format(inode_data.size - len(bytes)))
            print("Inode Values should be updated\n")

    if update:
        if (verbose):
            print("Updating Inode Length Field...\n")
        file_system_metadata = extract_values_fsstat(imagepath=image_location, offset=str(partition_to_use.start),
                                                     verbose=verbose)

        inode_offset = calculate_offset_inode(inode_num=inode_number, offset_partition=partition_to_use.start,
                                              file_system_metadata=file_system_metadata,
                                              sector_size=partition_to_use.sector_size, verbose=verbose)
        modifyFileLength(inode_offset, image_location, len(bytes))

    command.remove(["tempfile", "newfile", "places.sqlite", "places.sqlite-shm", "places.sqlite-wal"])
    modify_binary(blocks=inode_data.blocks, bytes_array=bytes, image_location=image_location,
                  fs_meta=file_system_metadata, sector_size=partition_to_use.sector_size,
                  partition_start=partition_to_use.start, verbose=verbose)
    return 0


def modify_binary(blocks, bytes_array, image_location, fs_meta, sector_size, partition_start, verbose=False):
    """
    This Python function writes back binary data in a specified image file at specific block offsets based
    on provided parameters.
    
    :param blocks: Block numbers of the inode
    :param bytes_array: Unused
    :param image_location: The `image_location` parameter in the `modify_binary` function is the file
    path to the image file that you want to modify. This function seems to be designed to write binary
    data to specific blocks within the image file based on the provided parameters
    :param fs_meta: Unused
    :param sector_size: The `sector_size` parameter in the `modify_binary` function represents the size
    of a sector on the storage device. It is used to calculate the offset for a specific block within
    the file system. The sector size is important for determining the alignment of data within the
    storage device and ensuring efficient read and
    :param partition_start: The `partition_start` parameter in the `modify_binary` function represents
    the starting offset of the partition within the disk image where the file system is located. This
    offset is used to calculate the absolute block address within the disk image when modifying binary
    data within specific blocks of the file system
    :param verbose: The `verbose` parameter in the `modify_binary` function is a boolean flag that
    controls whether additional information and debug messages should be printed during the execution of
    the function. If `verbose` is set to `True`, the function will print out details such as block
    offsets, bytes being written to blocks, defaults to False (optional)
    """
    pagesize = get_pagesize()
    byte_num = 0
    with (open(image_location, "r+b") as f):
        blocksize = int(fs_meta.block_size)
        for block in blocks:
            # Edgecase: Block Number 0 from istat
            if (block == 0):
                if (verbose):
                    print("Block Number 0 detected! We are not gonna overwrite the ext4 superblock!")
                break
            blockaddress = calculate_offset_block(block_num=block, offset_partition=partition_start,
                                                  file_system_metadata=fs_meta, sector_size=sector_size)
            if (verbose):
                print(f"The offset for block {block} is {blockaddress}")
            usable_adress = blockaddress // pagesize * pagesize
            if verbose:
                print(f"But the offset we are gonna use is {usable_adress}")
            mm = mmap.mmap(f.fileno(), pagesize, offset=usable_adress)
            bytestart = byte_num
            zero_byte_counter = 0
            wrote_byte = False
            for i in range(blocksize):
                if (byte_num >= len(bytes_array)):
                    zero_byte_counter += 1
                    mm[i] = 0
                else:
                    wrote_byte = True
                    mm[i] = bytes_array[byte_num]
                byte_num += 1
            if (verbose):
                if zero_byte_counter == 0:
                    print(f"Wrote bytes {bytestart} till {byte_num - 1} to the block\n")
                elif wrote_byte:
                    print(f"Wrote bytes {bytestart} till {byte_num - 1 - zero_byte_counter} to the block. Also filled the block with {zero_byte_counter} zero bytes.\n")
                else:
                    print(f"No data bytes written. Filled the block with {zero_byte_counter} zero bytes.\n")
            mm.flush()
            mm.close()
        f.close()
        was_usefull_data_lost = False
        for i in range(byte_num, len(bytes_array)):
            if not bytes_array[i] == 0:
                was_usefull_data_lost = True
        if (byte_num < len(bytes_array)):
            if was_usefull_data_lost:
                print("Error the file you wanted to write was to large")
                print("{} Bytes couldn't be written".format(len(bytes_array) - byte_num))
                print("Bytenum: {}".format(byte_num))
                print("Len Byte Array: {}".format(len(bytes_array)))
                file_to_large(len(bytes_array) - byte_num)
            else:
                print("Error the file you wanted to write was to large")
                print("But nothing broke cause there where only Zero Bytes")
