# swap_timestamps()
The function `swap_timestamps` swaps timestamps between two files at specified offsets within a
    memory-mapped image file.

## Parameters:
    def swap_timestamps(file_A_inode_offset, file_B_inode_offset, image_location, verbose=False):
-  file_A_inode_offset: The `file_A_inode_offset` parameter in the `swap_timestamps` function
    represents the offset of the inode for file A within the image file. This offset is used to locate
    the specific inode of file A within the image file
-  file_B_inode_offset: The `file_B_inode_offset` parameter in the `swap_timestamps` function
    represents the offset within the disk image where the metadata of file B is located. This offset is
    used to locate the specific timestamps within file B's metadata that need to be swapped with the
    corresponding timestamps in file A's metadata
-  image_location: The `image_location` parameter in the `swap_timestamps` function refers to
    the location of the image file that is being manipulated. This parameter should be a string
    representing the file path to the image file
-  verbose: The `verbose` parameter in the `swap_timestamps` function is a boolean flag that
    controls whether additional information or messages should be displayed during the execution of the
    function. When `verbose` is set to `True`, the function may print out progress updates, debug
    information, or any other relevant details, defaults to False (optional)

## Workflow:
1. For each offset of a timestamp do:
   1. Open file:
      1. Calculate Usable Offsets for A and B
      2. Open mmap pointer for A and B
      3. Save timestamp of A in temp
      4. Write timestamp of B in A
      5. Write timestamp of temp in B
      6. Close mmap A and B
   