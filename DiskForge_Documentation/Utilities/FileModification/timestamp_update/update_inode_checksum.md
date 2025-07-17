# update_inode_checksum()
This Python function updates the checksum of an inode in a file system image at a specific offset.

## Parameters:
    def update_inode_checksum(inode_offset,image_location,crc32c_inode_checksum):
    :param inode_offset: The `inode_offset` parameter in the `update_inode_checksum` function represents
    the offset in the image file where the inode is located. This offset is used to locate the specific
    inode within the file for updating its checksum
    :param image_location: The `image_location` parameter in the `update_inode_checksum` function is the
    file path of the image file that needs to be updated with the new checksum for a specific inode.
    This function reads the image file, locates the specific inode offset within the file, and updates
    the checksum values at the
    :param crc32c_inode_checksum: The `crc32c_inode_checksum` parameter is a list containing 4 elements. They contain the bytes of the checksum

## Workflow:
1. Extract pagesize
2. Open file
3. Open mmap pointer to inode
4. Write bytes to checksum fields