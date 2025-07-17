# null_inode()
The function `null_inode` writes zeros to a specified inode in a file system image at a given
    offset.

## Parameters:
    def null_inode(file_inode_offset, image_location, inode_size=256):
-  file_inode_offset: The `file_inode_offset` parameter in the `null_inode` function represents
    the offset of the file's inode within the disk image. This offset is used to locate and modify the
    inode data of the file within the disk image
-  image_location: The `image_location` parameter in the `null_inode` function is the path to
    the image file that contains the inode data. This function seems to be designed to nullify a
    specific inode within the image file by writing zeros to the corresponding inode data in the file
-  inode_size: The `inode_size` parameter in the `null_inode` function specifies the size of the
    inode that will be written as binary zeros to the specified file inode offset in the image file. The
    default value for `inode_size` is set to 256 bytes if no value is provided when calling the
    function, defaults to 256 (optional)

## Workflow:
1. Open file:
   1. Get Offset Off Inode
   2. Overwrite each byte with zero