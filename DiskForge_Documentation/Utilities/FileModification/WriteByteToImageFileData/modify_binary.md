# modify_binary()
This Python function writes back binary data in a specified image file at specific block offsets based
    on provided parameters.

## Parameters:
    def modify_binary(blocks, bytes_array, image_location, fs_meta, sector_size, partition_start, verbose=False):
-  blocks: Block numbers of the inode
-  bytes_array: Unused
-  image_location: The `image_location` parameter in the `modify_binary` function is the file
    path to the image file that you want to modify. This function seems to be designed to write binary
    data to specific blocks within the image file based on the provided parameters
-  fs_meta: Unused
-  sector_size: The `sector_size` parameter in the `modify_binary` function represents the size
    of a sector on the storage device. It is used to calculate the offset for a specific block within
    the file system. The sector size is important for determining the alignment of data within the
    storage device and ensuring efficient read and
-  partition_start: The `partition_start` parameter in the `modify_binary` function represents
    the starting offset of the partition within the disk image where the file system is located. This
    offset is used to calculate the absolute block address within the disk image when modifying binary
    data within specific blocks of the file system
-  verbose: The `verbose` parameter in the `modify_binary` function is a boolean flag that
    controls whether additional information and debug messages should be printed during the execution of
    the function. If `verbose` is set to `True`, the function will print out details such as block
    offsets, bytes being written to blocks, defaults to False (optional)

## Workflow:
1. Extract pagesize
2. Open file:
   1. For each block do:
      1. Check if block is not 0
      2. Write bytes to block
3. Check if no non 0 bytes were not written back
