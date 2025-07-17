# read_inode()
The `read_inode` function reads inode data from a disk image file, inserts zero bytes at specific positions, and returns the modified inode data.
## Parameters:
    def read_inode(full_offset, disk_image):
- full_offset: The `full_offset` parameter in the `read_inode` function represents the position
    of the inode on the disk image. It is the offset at which the inode data starts within the disk
    image file. This offset is used to locate and read the specific inode data from the disk image file
- disk_image: The `disk_image` parameter in the `read_inode` function is the path to the disk
    image file from which the inode data will be read. This file is assumed to contain the data
    representing the disk's contents, including the inodes. The function opens this file in binary mode
    ('rb')
- **return:** The function `read_inode` reads inode data from a disk image file at a specified offset. It
    reads a total of 256 bytes of data from the disk image file starting at the given offset. The
    function then inserts zero bytes at specific positions within the inode data before returning the
    modified inode data as a bytes object.

## Workflow:
1. Open disk image using `rb` mode
2. read `124` bytes
3. Insert `2` zero bytes for checksum
4. read 4 bytes
5. add 2 zero bytes
6. read rest