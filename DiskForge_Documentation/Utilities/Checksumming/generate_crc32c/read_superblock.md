# read_superblock()
The function `read_superblock` reads and returns the superblock data from a disk image starting at a specified offset within a partition.
## Parameters:
    def read_superblock(offset_partition, disk_image):
- offset_partition: The `offset_partition` parameter in the `read_superblock` function
    represents the starting offset of the partition within the disk image where the superblock is
    located. This offset is used to calculate the total offset to jump to the superblock within the disk
    image
- disk_image: The `disk_image` parameter refers to the path of the disk image file from which
    you want to read the superblock. This file contains the binary data representing the disk's
    contents, including the superblock information. You need to provide the full path to the disk image
    file as a string when calling
- **return:** The function `read_superblock` returns the superblock data read from the disk image
    starting at the specified offset. The superblock data is read as a binary string of length 1020
    bytes.

## Workflow:
1. Calculate Offset of superblock
2. read its bytes