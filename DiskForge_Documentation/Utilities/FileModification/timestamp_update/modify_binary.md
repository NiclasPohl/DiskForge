# modify_binary()
This Python function modifies binary data in a specified file at specific offsets based on provided
    timestamps.

## Parameters:
    def modify_binary(inode_offset, timestamp_offset, image_location, what_timestamp, timestamps_original, verbose=False, time=None):
-  inode_offset: The `inode_offset` parameter in the `modify_binary` function represents the
    offset where the inode information is located within the image file. This offset is used to locate
    the specific inode within the file system image
-  timestamp_offset: The `timestamp_offset` parameter in the `modify_binary` function represents
    the offset within the memory-mapped file where the timestamp data is located. This offset is used to
    locate the specific timestamp within the file that needs to be modified
-  image_location: The `image_location` parameter in the `modify_binary` function represents the
    location of the image file that you want to modify. This function opens the specified image file in
    read and write mode ("r+b") to perform modifications on it
-  what_timestamp: The `what_timestamp` parameter is used to determine which timestamp to modify
    in the binary file. It is an integer value that corresponds to different types of timestamps
-  timestamps_original: The `timestamps_original` parameter is a structure
    containing different timestamps related to a file. This object has attributes like `accessed`, `file_modified`, `inode_modified`, and
    `file_created`, each of which holds a timestamp value
-  verbose: The `verbose` parameter in the `modify_binary` function is a boolean flag that
    controls whether additional information and debug messages should be printed during the execution of
    the function. If `verbose` is set to `True`, the function will print out various details like the
    usable offset, usable index, hex, defaults to False (optional)
-  time: The `time` parameter in the `modify_binary` function is used to specify a new timestamp
    value that will be written into a binary file at a specific offset. This timestamp value will be
    converted to hexadecimal format and then written into the binary file at the appropriate location

## Workflow:
1. Extract pagesize
2. Calculate Offset of Timestamp and extra Timestamp
3. Convert timestamp to bytes
4. Write timestamps via mmap