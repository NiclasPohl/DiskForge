# modifyFileLength()
This function modifies the length of a file in a specific location within a memory-mapped file.

## Parameters:
    def modifyFileLength(file_inode_offset, image_location, newlength):
-  file_inode_offset: The `file_inode_offset` parameter in the `modifyFileLength` function
    represents the offset of the file's inode within the file system. This offset is used to locate
    specific information about the file, such as its length, within the file system structure
-  image_location: The `image_location` parameter in the `modifyFileLength` function represents
    the location of the file in which you want to modify the file length. This is the path to the file
    that you want to work with
-  newlength: The `newlength` parameter in the `modifyFileLength` function represents the new
    length that you want to set for a file. This length is converted to a byte representation using 8
    bytes in little-endian byte order before being written to specific offsets within the file specified
    by `file_inode_offset

## Workflow:
1. Extract Pagesize
2. Convert Newlength to bytes
3. Open mmap at offsets of both length fields in the inode
4. Copy bytes to the corresponding field