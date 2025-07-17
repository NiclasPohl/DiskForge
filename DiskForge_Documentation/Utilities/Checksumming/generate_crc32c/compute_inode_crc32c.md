# compute_inode_crc32c()
The function `compute_inode_crc32c` reads inode data from a disk image, serializes it with inode
    number and filesystem UUID, and computes a CRC32C checksum.

## Parameters:
    def compute_inode_crc32c(inode_number, offset_partition, offset_inode, disk_image):
- inode_number: The `inode_number` parameter is the unique identifier for an inode in a
    filesystem. It is used to locate and access specific metadata information about a file or directory
    stored on the disk
- offset_partition: The `offset_partition` parameter typically refers to the starting offset of
    a partition within a disk image. This offset is used to locate the specific partition on the disk
    image where the file system is stored. It is important for reading data related to the file system,
    such as the UUID (Universally Unique
- offset_inode: The `offset_inode` parameter typically refers to the location of the inode
    within the disk image. It is the offset value that points to the starting position of the inode data
    on the disk. This value is used to locate and read the inode data from the disk image
- disk_image: The `disk_image` parameter in the `compute_inode_crc32c` function is typically a
    binary representation of the disk or partition from which you are reading the inode data. It could
    be a file containing the raw data of the disk or partition, allowing you to read specific sectors or
    blocks to extract
- **return:** The function `compute_inode_crc32c` returns the CRC32C checksum computed for the serialized
    inode data along with the inode number and filesystem UUID.

## Workflow:
1. `compute_inode_crc32c` calls `read_inode`, `read_generation` and `read_uuid`
2. Next calls `serialize_inode(inode_data, inode_number, filesystem_uuid, generation_data)`
3. `crc32c_checksum = convert_crc32c(crc32c.crc32c(serialized_inode))`