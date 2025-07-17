# copy_timestamps()
The function `copy_timestamps` copies timestamps from one file to another using memory mapping in
    Python.

## Parameters:
    def copy_timestamps(file_A_inode_offset, file_B_inode_offset, image_location_src, image_location_target, verbose):
-  file_A_inode_offset: The `file_A_inode_offset` parameter in the `copy_timestamps` function
    represents the offset of the inode of file A within the disk image. This offset is used to locate
    the specific inode of file A within the disk image
-  file_B_inode_offset: The `file_B_inode_offset` parameter in the `copy_timestamps` function
    represents the offset of the inode of file B within the disk image. This offset is used to locate
    the specific inode of file B within the disk image file
-  image_location_src: The `image_location_src` parameter in the `copy_timestamps` function
    refers to the location of the source image file from which timestamps will be copied. This parameter
    should be a string representing the file path of the source image file
-  image_location_target: The `image_location_target` parameter in the `copy_timestamps`
    function is the file path to the target image where the timestamps will be copied to. This function
    seems to be copying timestamps from one file (specified by `file_A_inode_offset`) to another file
    (specified by `file_B_inode)
-  verbose: The `verbose` parameter in the `copy_timestamps` function is used to control whether
    additional information or messages should be displayed during the execution of the function. If
    `verbose` is set to `True`, you can include print statements or logging to provide more details
    about the progress or any relevant information

## Workflow:
1. For each timestamp offset do:
   1. Open File:
      1. Calculate A and B offsets
      2. Open mmap for A and B
      3. Copy timestamp from B to A
      4. Close mmap for A and B