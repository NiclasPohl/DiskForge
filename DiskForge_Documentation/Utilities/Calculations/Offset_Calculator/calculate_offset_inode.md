# calculate_offset_inode()

    def calculate_offset_inode(inode_num, offset_partition: int, file_system_metadata, sector_size: int, verbose=False):

This Python function calculates the offset of a specific inode within a file system partition.
    
- inode_num: The `inode_num` parameter represents the inode number for which you want to calculate the offset within the file system
- offset_partition: The `offset_partition` parameter in the `calculate_offset_inode` function
    represents the offset of the partition where the file system is located. This offset is typically
    measured in sectors and is used to calculate the absolute offset of a specific inode within the file
    system
    - :type offset_partition: int
- file_system_metadata: The `file_system_metadata` parameter seems to contain information about
    the file system, such as the number of inodes per group, inode size, block size, blocks per group,
    and the start of inode tables for each group
- sector_size: Sector size is the size of a sector on a storage device, typically measured in
    bytes. It is a fundamental unit of data storage on a disk
    - :type sector_size: int
- verbose: The `calculate_offset_inode` function takes in several parameters to calculate the
    offset of a specific inode within a filesystem. Here's a brief explanation of each parameter:,
    defaults to False (optional)
- **return:** the full offset of a specific inode within a filesystem, taking into account the inode
    number, offset partition, filesystem metadata, sector size, and whether verbose output is enabled.

Workflow:

1. Extract Metadata Parameters
2. Calculate Parameters
   1. *index_inode* = (inode_num - 1) % inodes_per_group
   2. *offset_inode_to_inode_table* = index_inode * inode_size
   3. *inode_group* = (inode_num - 1) // inodes_per_group
   4. *offset_inode_table_to_block_begin* = begin_inode_table * block_size
   5. *group_offset* = inode_group * blocks_per_group * block_size
   6. *fulloffset* = begin_inode_table * block_size + index_inode * inode_size + int(offset_partition) * int(sector_size)