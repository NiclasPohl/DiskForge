# calculate_offset_block()

    def calculate_offset_block(block_num: int, offset_partition: int, file_system_metadata, sector_size: int):

This Python function calculates the offset of a block within a file system based on the block number, offset within a partition, file system metadata, and sector size.
    
-  block_num: The `block_num` parameter represents the number of the block within the file
    system
    - :type block_num: int
-  offset_partition: The `offset_partition` parameter represents the offset within a partition.
    It is used to calculate the offset within a block based on the block number, sector size, and file
    system metadata
    - :type offset_partition: int
-  file_system_metadata: The `file_system_metadata` parameter seems to contain information about
    the file system, including the block size. To use this information in the `calculate_offset_block`
    function, you can extract the block size from the `file_system_metadata` and use it in the
    calculation
-  sector_size: The `sector_size` parameter represents the size of a sector in bytes on the
    storage device. It is typically a power of 2 value, such as 512 bytes or 4096 bytes, depending on
    the storage device's specifications
    - :type sector_size: int
- **return:** The function `calculate_offset_block` returns the full offset calculated based on the block
    number, offset partition, file system metadata, and sector size provided as input parameters.

Workflow:

1. *fulloffset* = block_num * block_size + offset_partition * sector_size