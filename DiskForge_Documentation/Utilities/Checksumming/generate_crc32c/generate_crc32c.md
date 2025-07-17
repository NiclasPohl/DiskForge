# generate_crc32c.py

The provided Python script contains functions to read and manipulate inode data, UUID, superblock data, and compute CRC32C checksum for serialized inode data in a disk image file.

This file contains the following functions:
- [read_inode()](./read_inode.md)
- [read_uuid()](./read_uuid.md)
- [read_superblock()](./read_superblock.md)
- [read_generation()](./read_generation.md)
- [serialize_inode()](./serialize_inode.md)
- [convert_crc32c()](./convert_crc32c.md)
- [compute_inode_crc32c()](./compute_inode_crc32c.md)

## Workflow:
1. `compute_inode_crc32c` calls `read_inode`, `read_generation` and `read_uuid`
2. Next calls `serialize_inode(inode_data, inode_number, filesystem_uuid, generation_data)`
3. `crc32c_checksum = convert_crc32c(crc32c.crc32c(serialized_inode))`