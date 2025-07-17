# shift_binary()
This Python function reads a specific timestamp from a memory-mapped file, converts it to a Unix
    timestamp, shifts it by a specified amount, converts it back to a hexadecimal representation, and
    writes the updated timestamp back to the file.

## Parameters:
    def shift_binary(inode_offset, timestamp_offset, image_location, what_timestamp, timestamps_original, second_shift,verbose=False):
-  inode_offset: The `inode_offset` parameter in the `shift_binary` function represents the
    offset value for the inode within the file system image. It is used to calculate the memory address
    where the timestamp data is located within the file system image
-  timestamp_offset: The `timestamp_offset` parameter in the `shift_binary` function represents
    the offset within the memory-mapped file where the timestamp data is located. This offset is added
    to the `inode_offset` to determine the exact location of the timestamp data within the file. The
    function reads the timestamp data from this
-  image_location: The `image_location` parameter in the `shift_binary` function refers to the
    location of the image file that you want to manipulate. This function reads the image file in binary
    mode and performs operations on it based on the other parameters provided
-  what_timestamp: The `what_timestamp` parameter is used to determine which timestamp to
    modify
-  timestamps_original: The `timestamps_original` parameter is a structure
    containing different timestamps related to a file. This object has attributes like `accessed`, `file_modified`, `inode_modified`, and
    `file_created`, each of which holds a timestamp value
-  second_shift: The `second_shift` parameter in the `shift_binary` function represents the
    number of seconds by which you want to shift the timestamp. This value will be added to the current
    Unix timestamp of the specified timestamp type (accessed, file_modified, inode_modified, or
    file_created) before updating the timestamp
-  verbose: The `verbose` parameter in the `shift_binary` function is a boolean flag that
    controls whether additional information and debug messages should be printed during the execution of
    the function. If `verbose` is set to `True`, the function will print out details such as the usable
    offset, usable index, hex, defaults to False (optional)

## Workflow:
1. Extract pagesize
2. Open File
   1. Calculate Timestamp Offset
   2. Extract Timestamp
3. Shift Timestamp
4. Write Timestamp back using mmap