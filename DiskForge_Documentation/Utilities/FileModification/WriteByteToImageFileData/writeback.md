# writeback()
The function `writeback` performs various operations related to updating inode data and file
    contents in a file system image.

## Parameters:
    def writeback(image_location, partition_to_use, inode_number, file_path, verbose, update):
-  image_location: The `image_location` parameter refers to the location of the image file you
    are working with. This could be the path to a disk image or a similar file that contains the
    filesystem you are analyzing or modifying
-  partition_to_use: The `partition_to_use` parameter in the `writeback` function is used to
    specify the partition on which the file system metadata and inode data are located. It contains
    information such as the start offset of the partition and the sector size of the partition. This
    information is crucial for extracting and modifying data
-  inode_number: The `inode_number` parameter in the `writeback` function represents the unique
    identifier of an inode in a file system. The inode contains metadata about a specific file or
    directory, such as permissions, timestamps, and pointers to data blocks
-  file_path: The `file_path` parameter in the `writeback` function is the path to the file that
    will be hexdumped and its bytes will be extracted for comparison with the inode data
-  verbose: The `verbose` parameter in the `writeback` function is used to control whether
    additional information and messages should be printed during the execution of the function. If
    `verbose` is set to `True`, the function will print out various messages to provide more details
    about the process. If `verbose`
-  update: The `update` parameter in the `writeback` function is a boolean flag that determines
    whether to update the Inode Length Field or not. If `update` is set to `True`, the function will
    proceed with updating the Inode Length Field. If `update` is set to `False
- **return:** The function `writeback` is returning the integer value `0`.

## Workflow:
1. Extract Metadata
2. Compare Inode Length to new file length
   1. If Equal everything is good
   2. If inode length greater then everything good, maybe update inode size
   3. Else: Bad possible problem
3. Execute modify binary 