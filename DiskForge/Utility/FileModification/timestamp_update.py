import mmap
import time

from Utility.SleuthKit.ExtractValuesFromIstat import convert_istat_to_timestamp
from Utility.Conversions.TimeConverter import time_to_hex, unixtime_to_hex
import Utility.Other.Terminal_Commands as commando
from Utility.Other.WriteTimeModLog import changedMetadata


def get_pagesize():
    """
    The function `get_pagesize` retrieves the page size configuration value and returns it as an
    integer.
    :return: The function `get_pagesize` is returning the page size value retrieved from the system
    configuration using the `commando.getconf("PAGE_SIZE")` command. The value is then converted to an
    integer before being returned.
    """
    result = commando.getconf("PAGE_SIZE")
    result = int(result.stdout)
    return result

def timestamp_update(timestamps_to_modify, inode_offset, image_location, timestamps_original, verbose=False, time=None):
    """
    The function `timestamp_update` modifies timestamps in a file system image based on the specified
    criteria.
    
    :param timestamps_to_modify: `timestamps_to_modify` is a parameter that specifies which timestamps
    to modify. It can be a string indicating a single timestamp type to modify (e.g., "accessed",
    "file_modified", "inode_modified", "file_created", "all"), or a list of strings containing multiple
    timestamp types to modify
    :param inode_offset: The `inode_offset` parameter in the `timestamp_update` function is used to
    specify the offset of the inode within the file system. This offset is crucial for locating and
    updating the metadata associated with the specified inode
    :param image_location: The `image_location` parameter in the `timestamp_update` function represents
    the location of the image where the timestamps are being modified. This could be a file path or any
    other identifier that specifies the location of the image data
    :param timestamps_original: Unused
    :param verbose: The `verbose` parameter in the `timestamp_update` function is a boolean flag that
    controls whether additional information or messages should be displayed during the execution of the
    function. When `verbose` is set to `True`, the function may print out more details or status updates
    to the console to provide feedback on, defaults to False (optional)
    :param time: The `time` parameter in the `timestamp_update` function is used to specify a specific
    time to update the timestamps to. It can be a single timestamp value or a list of timestamp values
    corresponding to the timestamps to be modified. The function uses this parameter to update the
    specified timestamps in the binary data
    """
    changedMetadata((timestamps_to_modify, inode_offset))
    if isinstance(timestamps_to_modify, str):
        match timestamps_to_modify.lower():
            case "accessed":
                accessed = True
                modify_binary(int(inode_offset), 8, image_location, 0, timestamps_original, verbose=verbose, time=time)
            case "file_modified":
                file_modified = True
                modify_binary(int(inode_offset), 16, image_location, 1, timestamps_original, verbose=verbose, time=time)
            case "inode_modified":
                inode_modified = True
                modify_binary(int(inode_offset), 12, image_location, 2, timestamps_original, verbose=verbose, time=time)
            case "file_created":
                file_created = True
                modify_binary(int(inode_offset), 144, image_location, 3, timestamps_original, verbose=verbose,
                              time=time)
            case "all":
                print("all")
                print("all")
                modify_binary(int(inode_offset), 8, image_location, 0, timestamps_original, verbose=verbose, time=time)
                modify_binary(int(inode_offset), 16, image_location, 1, timestamps_original, verbose=verbose, time=time)
                modify_binary(int(inode_offset), 12, image_location, 2, timestamps_original, verbose=verbose, time=time)
                modify_binary(int(inode_offset), 144, image_location, 3, timestamps_original, verbose=verbose,
                              time=time)
    else:
        for i in range(len(timestamps_to_modify)):
            print(timestamps_to_modify[i].lower())
            print(type(time))
            if isinstance(time, list):
                tmp = time[i]
            else:
                tmp = time
            match timestamps_to_modify[i].lower():
                case "accessed":
                    accessed = True
                    modify_binary(int(inode_offset), 8, image_location, 0, timestamps_original, verbose=verbose,
                                  time=tmp)
                case "file_modified":
                    file_modified = True
                    modify_binary(int(inode_offset), 16, image_location, 1, timestamps_original, verbose=verbose,
                                  time=tmp)
                case "inode_modified":
                    inode_modified = True
                    modify_binary(int(inode_offset), 12, image_location, 2, timestamps_original, verbose=verbose,
                                  time=tmp)
                case "file_created":
                    file_created = True
                    modify_binary(int(inode_offset), 144, image_location, 3, timestamps_original, verbose=verbose,
                                  time=tmp)
                case "all":
                    modify_binary(int(inode_offset), 8, image_location, 0, timestamps_original, verbose=verbose,
                                  time=tmp)
                    modify_binary(int(inode_offset), 16, image_location, 1, timestamps_original, verbose=verbose,
                                  time=tmp)
                    modify_binary(int(inode_offset), 12, image_location, 2, timestamps_original, verbose=verbose,
                                  time=tmp)
                    modify_binary(int(inode_offset), 144, image_location, 3, timestamps_original, verbose=verbose,
                                  time=tmp)


def timestamp_shift(timestamps_to_modify, inode_offset, image_location, timestamps_original, second_shift,verbose=False):
    """
    The function `timestamp_shift` modifies specified timestamps in a file system image based on the
    provided parameters.
    
    :param timestamps_to_modify: timestamps_to_modify is a list of strings indicating which timestamps
    to modify. Possible values include "accessed", "file_modified", "inode_modified", "file_created",
    and "all"
    :param inode_offset: The `inode_offset` parameter in the `timestamp_shift` function represents the
    offset value for the inode being modified. It is used to calculate the specific location within the
    image where the timestamps are stored for that particular inode
    :param image_location: The `image_location` parameter in the `timestamp_shift` function represents
    the location of the image where the timestamps are being modified. This could be a file path or any
    other identifier that specifies the location of the image data
    :param timestamps_original: Unused
    :param second_shift: The `second_shift` parameter in the `timestamp_shift` function is used as an offset value for shifting timestamps. It is likely used to adjust the timestamps by a
    certain number of seconds during the shifting process. This parameter allows for flexibility in how
    much the timestamps are shifted by
    :param verbose: The `verbose` parameter in the `timestamp_shift` function is a boolean parameter
    that is set to `False` by default. It is used to control whether additional information or details
    should be displayed during the execution of the function. If `verbose` is set to `True`, the
    function may output, defaults to False (optional)
    """
    changedMetadata((timestamps_to_modify, inode_offset))
    for i in range(len(timestamps_to_modify)):
        match timestamps_to_modify[i].lower():
            case "accessed":
                accessed = True
                shift_binary(int(inode_offset), 8, image_location, 0, timestamps_original, second_shift,
                             verbose=verbose)
            case "file_modified":
                file_modified = True
                shift_binary(int(inode_offset), 16, image_location, 1, timestamps_original, second_shift,
                             verbose=verbose)
            case "inode_modified":
                inode_modified = True
                shift_binary(int(inode_offset), 12, image_location, 2, timestamps_original, second_shift,
                             verbose=verbose)
            case "file_created":
                file_created = True
                shift_binary(int(inode_offset), 144, image_location, 3, timestamps_original, second_shift,
                             verbose=verbose)
            case "all":
                shift_binary(int(inode_offset), 8, image_location, 0, timestamps_original, second_shift,
                             verbose=verbose)
                shift_binary(int(inode_offset), 16, image_location, 1, timestamps_original, second_shift,
                             verbose=verbose)
                shift_binary(int(inode_offset), 12, image_location, 2, timestamps_original, second_shift,
                             verbose=verbose)
                shift_binary(int(inode_offset), 144, image_location, 3, timestamps_original, second_shift,
                             verbose=verbose)


def shift_binary(inode_offset, timestamp_offset, image_location, what_timestamp, timestamps_original, second_shift,verbose=False):
    """
    This Python function reads a specific timestamp from a memory-mapped file, converts it to a Unix
    timestamp, shifts it by a specified amount, converts it back to a hexadecimal representation, and
    writes the updated timestamp back to the file.
    
    :param inode_offset: The `inode_offset` parameter in the `shift_binary` function represents the
    offset value for the inode within the file system image. It is used to calculate the memory address
    where the timestamp data is located within the file system image
    :param timestamp_offset: The `timestamp_offset` parameter in the `shift_binary` function represents
    the offset within the memory-mapped file where the timestamp data is located. This offset is added
    to the `inode_offset` to determine the exact location of the timestamp data within the file. The
    function reads the timestamp data from this
    :param image_location: The `image_location` parameter in the `shift_binary` function refers to the
    location of the image file that you want to manipulate. This function reads the image file in binary
    mode and performs operations on it based on the other parameters provided
    :param what_timestamp: The `what_timestamp` parameter is used to determine which timestamp to
    modify
    :param timestamps_original: The `timestamps_original` parameter is a structure
    containing different timestamps related to a file. This object has attributes like `accessed`, `file_modified`, `inode_modified`, and
    `file_created`, each of which holds a timestamp value
    :param second_shift: The `second_shift` parameter in the `shift_binary` function represents the
    number of seconds by which you want to shift the timestamp. This value will be added to the current
    Unix timestamp of the specified timestamp type (accessed, file_modified, inode_modified, or
    file_created) before updating the timestamp
    :param verbose: The `verbose` parameter in the `shift_binary` function is a boolean flag that
    controls whether additional information and debug messages should be printed during the execution of
    the function. If `verbose` is set to `True`, the function will print out details such as the usable
    offset, usable index, hex, defaults to False (optional)
    """
    pagesize = get_pagesize()
    # Offset = ADRESSE//PAGESIZE
    # Index = ADRESSE % PAGESIZE
    # EDGECASE: INDEX + 8 >= PAGESIZE TODO rausfinden ob relevant
    with open(image_location, "r+b") as f:
        adress = inode_offset + timestamp_offset
        usable_offset = adress // pagesize * pagesize
        usable_index = adress % pagesize
        if verbose:
            print("\n Usable Offset: " + str(usable_offset))
            print("Usable Index: " + str(usable_index))
        mm = mmap.mmap(f.fileno(), pagesize, offset=usable_offset)
        if verbose:
            print("Hex Value of the Timestamp: " + str(mm[usable_index:usable_index + 4].hex()))
        timestamp = 0
        match what_timestamp:
            case 0:
                timestamp = convert_istat_to_timestamp(str(timestamps_original.accessed))
            case 1:
                timestamp = convert_istat_to_timestamp(str(timestamps_original.file_modified))
            case 2:
                timestamp = convert_istat_to_timestamp(str(timestamps_original.inode_modified))
            case 3:
                timestamp = convert_istat_to_timestamp(str(timestamps_original.file_created))
        unixtime = time.mktime(timestamp.timetuple())
        newtime = unixtime + second_shift
        hextime = unixtime_to_hex(newtime)
        bytetime = bytes.fromhex(hextime[2:])
        if verbose:
            print("HexTime: " + str(hextime))
            print("ByteTime: " + str(bytetime))
        # Convert to little Endian
        littleEndianTime = bytetime[::-1]
        mm[usable_index:usable_index + 4] = littleEndianTime
        # Save Changes
        mm.flush()
        mm.close()
        f.close()


def modify_binary(inode_offset, timestamp_offset, image_location, what_timestamp, timestamps_original, verbose=False, time=None):
    """
    This Python function modifies binary data in a specified file at specific offsets based on provided
    timestamps.
    
    :param inode_offset: The `inode_offset` parameter in the `modify_binary` function represents the
    offset where the inode information is located within the image file. This offset is used to locate
    the specific inode within the file system image
    :param timestamp_offset: The `timestamp_offset` parameter in the `modify_binary` function represents
    the offset within the memory-mapped file where the timestamp data is located. This offset is used to
    locate the specific timestamp within the file that needs to be modified
    :param image_location: The `image_location` parameter in the `modify_binary` function represents the
    location of the image file that you want to modify. This function opens the specified image file in
    read and write mode ("r+b") to perform modifications on it
    :param what_timestamp: The `what_timestamp` parameter is used to determine which timestamp to modify
    in the binary file. It is an integer value that corresponds to different types of timestamps
    :param timestamps_original: The `timestamps_original` parameter is a structure
    containing different timestamps related to a file. This object has attributes like `accessed`, `file_modified`, `inode_modified`, and
    `file_created`, each of which holds a timestamp value
    :param verbose: The `verbose` parameter in the `modify_binary` function is a boolean flag that
    controls whether additional information and debug messages should be printed during the execution of
    the function. If `verbose` is set to `True`, the function will print out various details like the
    usable offset, usable index, hex, defaults to False (optional)
    :param time: The `time` parameter in the `modify_binary` function is used to specify a new timestamp
    value that will be written into a binary file at a specific offset. This timestamp value will be
    converted to hexadecimal format and then written into the binary file at the appropriate location
    """
    pagesize = get_pagesize()
    with open(image_location, "r+b") as f:
        adress = inode_offset + timestamp_offset
        usable_offset = adress // pagesize * pagesize
        usable_index = adress % pagesize
        if verbose:
            print("\n Usable Offset: " + str(usable_offset))
            print("Usable Index: " + str(usable_index))
        mm = mmap.mmap(f.fileno(), pagesize, offset=usable_offset)

        microsecond_offset = 0
        if verbose:
            print("Hex Value of the Timestamp: " + str(mm[usable_index:usable_index + 4].hex()))
        match what_timestamp:
            case 0:
                print("Accessed Original: " + str(timestamps_original.accessed))
                microsecond_offset = 140
            case 1:
                print("File Modified Original: " + str(timestamps_original.file_modified))
                microsecond_offset = 136
            case 2:
                print("Inode Modified Original: " + str(timestamps_original.inode_modified))
                microsecond_offset = 132
            case 3:
                print("File Created Original: " + str(timestamps_original.file_created))
                microsecond_offset = 148

        t2h = time_to_hex(time, verbose)
        hextime = t2h[0]
        bytetime = bytes.fromhex(hextime[2:])
        if verbose:
            print("HexTime: " + str(hextime))
            print("ByteTime: " + str(bytetime))
        # Convert to little Endian
        littleEndianTime = bytetime[::-1]
        mm[usable_index:usable_index + 4] = littleEndianTime
        mm.flush()
        mm.close()

        adress = inode_offset + microsecond_offset
        usable_offset = adress // pagesize * pagesize
        usable_index = adress % pagesize

        mm = mmap.mmap(f.fileno(), pagesize, offset=usable_offset)

        t2h = t2h[1]
        mm[usable_index:usable_index + 4] = t2h
        # Save Changes
        mm.flush()
        mm.close()
        f.close()


# TODO zweite image Location
def swap_timestamps(file_A_inode_offset, file_B_inode_offset, image_location, verbose=False):
    """
    The function `swap_timestamps` swaps timestamps between two files at specified offsets within a
    memory-mapped image file.
    
    :param file_A_inode_offset: The `file_A_inode_offset` parameter in the `swap_timestamps` function
    represents the offset of the inode for file A within the image file. This offset is used to locate
    the specific inode of file A within the image file
    :param file_B_inode_offset: The `file_B_inode_offset` parameter in the `swap_timestamps` function
    represents the offset within the disk image where the metadata of file B is located. This offset is
    used to locate the specific timestamps within file B's metadata that need to be swapped with the
    corresponding timestamps in file A's metadata
    :param image_location: The `image_location` parameter in the `swap_timestamps` function refers to
    the location of the image file that is being manipulated. This parameter should be a string
    representing the file path to the image file
    :param verbose: The `verbose` parameter in the `swap_timestamps` function is a boolean flag that
    controls whether additional information or messages should be displayed during the execution of the
    function. When `verbose` is set to `True`, the function may print out progress updates, debug
    information, or any other relevant details, defaults to False (optional)
    """
    pagesize = get_pagesize()
    # Offset = ADRESSE//PAGESIZE
    # Index = ADRESSE % PAGESIZE
    # EDGECASE: INDEX + 8 >= PAGESIZE TODO rausfinden ob relevant
    offsets = [8, 12, 16, 144, 132, 136, 140, 148]
    for i in range(8):
        with open(image_location, "r+b") as f:
            '''Step 1: Get Addresses for both Files'''
            file_A_adress = file_A_inode_offset + offsets[i]
            file_A_usable_offset = file_A_adress // pagesize * pagesize
            file_A_usable_index = file_A_adress % pagesize

            file_B_adress = file_B_inode_offset + offsets[i]
            file_B_usable_offset = file_B_adress // pagesize * pagesize
            file_B_usable_index = file_B_adress % pagesize

            '''Create mmap for both'''
            file_A_mm = mmap.mmap(f.fileno(), pagesize, offset=file_A_usable_offset)
            file_B_mm = mmap.mmap(f.fileno(), pagesize, offset=file_B_usable_offset)

            '''Swap timestamp from B to A'''
            temp = file_A_mm[file_A_usable_index:file_A_usable_index + 4]
            file_A_mm[file_A_usable_index:file_A_usable_index + 4] = file_B_mm[
                                                                     file_B_usable_index:file_B_usable_index + 4]

            '''Close mmap and reopen first B than A cause if they are the same frame we would undo changes potentially'''
            file_B_mm.flush()
            file_B_mm.close()
            file_A_mm.flush()
            file_A_mm.close()
            file_B_mm = mmap.mmap(f.fileno(), pagesize, offset=file_B_usable_offset)

            '''Save Timestamp from A in B'''
            file_B_mm[file_B_usable_index:file_B_usable_index + 4] = temp
            file_B_mm.flush()
            file_B_mm.close()

            f.close()


def copy_timestamps(file_A_inode_offset, file_B_inode_offset, image_location_src, image_location_target, verbose):
    """
    The function `copy_timestamps` copies timestamps from one file to another using memory mapping in
    Python.
    
    :param file_A_inode_offset: The `file_A_inode_offset` parameter in the `copy_timestamps` function
    represents the offset of the inode of file A within the disk image. This offset is used to locate
    the specific inode of file A within the disk image
    :param file_B_inode_offset: The `file_B_inode_offset` parameter in the `copy_timestamps` function
    represents the offset of the inode of file B within the disk image. This offset is used to locate
    the specific inode of file B within the disk image file
    :param image_location_src: The `image_location_src` parameter in the `copy_timestamps` function
    refers to the location of the source image file from which timestamps will be copied. This parameter
    should be a string representing the file path of the source image file
    :param image_location_target: The `image_location_target` parameter in the `copy_timestamps`
    function is the file path to the target image where the timestamps will be copied to. This function
    seems to be copying timestamps from one file (specified by `file_A_inode_offset`) to another file
    (specified by `file_B_inode
    :param verbose: The `verbose` parameter in the `copy_timestamps` function is used to control whether
    additional information or messages should be displayed during the execution of the function. If
    `verbose` is set to `True`, you can include print statements or logging to provide more details
    about the progress or any relevant information
    """
    pagesize = get_pagesize()
    # Offset = ADRESSE//PAGESIZE
    # Index = ADRESSE % PAGESIZE
    # EDGECASE: INDEX + 8 >= PAGESIZE TODO rausfinden ob relevant
    offsets = [8, 12, 16, 144, 132, 136, 140, 148]
    for i in range(8):
        with open(image_location_src, "r+b") as src:
            with open(image_location_target, "r+b") as target:
                '''Step 1: Get Addresses for both Files'''
                file_A_adress = file_A_inode_offset + offsets[i]
                file_A_usable_offset = file_A_adress // pagesize * pagesize
                file_A_usable_index = file_A_adress % pagesize

                file_B_adress = file_B_inode_offset + offsets[i]
                file_B_usable_offset = file_B_adress // pagesize * pagesize
                file_B_usable_index = file_B_adress % pagesize

                '''Create mmap for both'''
                file_A_mm = mmap.mmap(src.fileno(), pagesize, offset=file_A_usable_offset)
                file_B_mm = mmap.mmap(target.fileno(), pagesize, offset=file_B_usable_offset)

                '''Copy timestamp from A to B'''
                file_B_mm[file_B_usable_index:file_B_usable_index + 4] = file_A_mm[
                                                                         file_A_usable_index:file_A_usable_index + 4]

                '''Close all mmaps and flush'''
                file_B_mm.flush()
                file_B_mm.close()
                file_A_mm.close()
                target.close()
            src.close()


def modifyFileLength(file_inode_offset, image_location, newlength):
    """
    This function modifies the length of a file in a specific location within a memory-mapped file.
    
    :param file_inode_offset: The `file_inode_offset` parameter in the `modifyFileLength` function
    represents the offset of the file's inode within the file system. This offset is used to locate
    specific information about the file, such as its length, within the file system structure
    :param image_location: The `image_location` parameter in the `modifyFileLength` function represents
    the location of the file in which you want to modify the file length. This is the path to the file
    that you want to work with
    :param newlength: The `newlength` parameter in the `modifyFileLength` function represents the new
    length that you want to set for a file. This length is converted to a byte representation using 8
    bytes in little-endian byte order before being written to specific offsets within the file specified
    by `file_inode_offset
    """
    pagesize = get_pagesize()
    byte_representation = newlength.to_bytes(8, byteorder='little')
    offsets = [4, 108]
    adress = file_inode_offset + 4
    usable_offset = adress // pagesize * pagesize
    usable_index = adress % pagesize
    with open(image_location, "r+b") as f:
        mm = mmap.mmap(f.fileno(), pagesize, offset=usable_offset)
        for i in range(4):
            mm[usable_index + i] = byte_representation[i]
        mm.flush()
        mm.close()

        adress = file_inode_offset + 108
        usable_offset = adress // pagesize * pagesize
        usable_index = adress % pagesize
        mm = mmap.mmap(f.fileno(), pagesize, offset=usable_offset)
        for i in range(4):
            mm[usable_index + i] = byte_representation[i + 4]
        mm.flush()
        mm.close()
        f.flush()


def null_inode(file_inode_offset, image_location, inode_size=256):
    """
    The function `null_inode` writes zeros to a specified inode in a file system image at a given
    offset.
    
    :param file_inode_offset: The `file_inode_offset` parameter in the `null_inode` function represents
    the offset of the file's inode within the disk image. This offset is used to locate and modify the
    inode data of the file within the disk image
    :param image_location: The `image_location` parameter in the `null_inode` function is the path to
    the image file that contains the inode data. This function seems to be designed to nullify a
    specific inode within the image file by writing zeros to the corresponding inode data in the file
    :param inode_size: The `inode_size` parameter in the `null_inode` function specifies the size of the
    inode that will be written as binary zeros to the specified file inode offset in the image file. The
    default value for `inode_size` is set to 256 bytes if no value is provided when calling the
    function, defaults to 256 (optional)
    """
    # INTERESTING
    changedMetadata((["Nuke"], file_inode_offset))
    pagesize = get_pagesize()
    with open(image_location, "r+b") as img:
        file_adress = file_inode_offset
        file_usable_offset = file_adress // pagesize * pagesize
        file_usable_index = file_adress % pagesize

        file_mm = mmap.mmap(img.fileno(), pagesize, offset=file_usable_offset)
        binary_zero = bytes(inode_size)
        file_mm[file_usable_index:file_usable_index + inode_size] = binary_zero
        file_mm.flush()
        file_mm.close()
        img.close()

def update_inode_checksum(inode_offset,image_location,crc32c_inode_checksum):
    """
    This Python function updates the checksum of an inode in a file system image at a specific offset.
    
    :param inode_offset: The `inode_offset` parameter in the `update_inode_checksum` function represents
    the offset in the image file where the inode is located. This offset is used to locate the specific
    inode within the file for updating its checksum
    :param image_location: The `image_location` parameter in the `update_inode_checksum` function is the
    file path of the image file that needs to be updated with the new checksum for a specific inode.
    This function reads the image file, locates the specific inode offset within the file, and updates
    the checksum values at the
    :param crc32c_inode_checksum: The `crc32c_inode_checksum` parameter seems to be a list or array
    containing 4 elements. In the provided code snippet, these elements are accessed using indices 0, 1,
    2, and 3 to update the checksum values at specific offsets within the memory-mapped file
    """
    pagesize = get_pagesize()
    with open(image_location, "r+b") as f:
        adress = inode_offset
        usable_offset = adress // pagesize * pagesize
        usable_index = adress % pagesize
        print(usable_index)

        mm = mmap.mmap(f.fileno(), pagesize, offset=usable_offset)


        mm[usable_index+124] = crc32c_inode_checksum[0]
        mm[usable_index+125] = crc32c_inode_checksum[1]
        mm[usable_index+130] = crc32c_inode_checksum[2]
        mm[usable_index+131] = crc32c_inode_checksum[3]


        # Save Changes
        mm.flush()
        mm.close()
        f.close()
