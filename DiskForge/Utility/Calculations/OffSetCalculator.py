def calculate_offset_inode(inode_num, offset_partition: int, file_system_metadata, sector_size: int, verbose=False):
    """
    This Python function calculates the offset of a specific inode within a file system partition.
    
    :param inode_num: The `inode_num` parameter represents the inode number for which you want to
    calculate the offset within the file system
    :param offset_partition: The `offset_partition` parameter in the `calculate_offset_inode` function
    represents the offset of the partition where the file system is located. This offset is typically
    measured in sectors and is used to calculate the absolute offset of a specific inode within the file
    system
    :type offset_partition: int
    :param file_system_metadata: The `file_system_metadata` parameter seems to contain information about
    the file system, such as the number of inodes per group, inode size, block size, blocks per group,
    and the start of inode tables for each group
    :param sector_size: Sector size is the size of a sector on a storage device, typically measured in
    bytes. It is a fundamental unit of data storage on a disk
    :type sector_size: int
    :param verbose: The `calculate_offset_inode` function takes in several parameters to calculate the
    offset of a specific inode within a filesystem. Here's a brief explanation of each parameter:,
    defaults to False (optional)
    :return: the full offset of a specific inode within a filesystem, taking into account the inode
    number, offset partition, filesystem metadata, sector size, and whether verbose output is enabled.
    """
    inodes_per_group = int(file_system_metadata.inodes_per_group)
    inode_size = int(file_system_metadata.inode_size)
    block_size = int(file_system_metadata.block_size)
    blocks_per_group = int(file_system_metadata.blocks_per_group)
    inode_num = int(inode_num)

    index_inode = (inode_num - 1) % inodes_per_group
    offset_to_inode_table = index_inode * inode_size
    inode_group = (inode_num - 1) // inodes_per_group
    begin_inode_table = int(file_system_metadata.inode_tables[inode_group].start)

    offset_inode_table_to_block_begin = begin_inode_table * block_size
    group_offset = inode_group * blocks_per_group * block_size
    inode_full_offset = group_offset + offset_inode_table_to_block_begin + offset_to_inode_table + int(
        offset_partition) * int(sector_size)

    fulloffset = begin_inode_table * block_size + index_inode * inode_size + int(offset_partition) * int(sector_size)
    return fulloffset


def calculate_offset_block(block_num: int, offset_partition: int, file_system_metadata, sector_size: int):
    """
    This Python function calculates the offset of a block within a file system based on the block
    number, offset within a partition, file system metadata, and sector size.
    
    :param block_num: The `block_num` parameter represents the number of the block within the file
    system
    :type block_num: int
    :param offset_partition: The `offset_partition` parameter represents the offset within a partition.
    It is used to calculate the offset within a block based on the block number, sector size, and file
    system metadata
    :type offset_partition: int
    :param file_system_metadata: The `file_system_metadata` parameter seems to contain information about
    the file system, including the block size. To use this information in the `calculate_offset_block`
    function, you can extract the block size from the `file_system_metadata` and use it in the
    calculation
    :param sector_size: The `sector_size` parameter represents the size of a sector in bytes on the
    storage device. It is typically a power of 2 value, such as 512 bytes or 4096 bytes, depending on
    the storage device's specifications
    :type sector_size: int
    :return: The function `calculate_offset_block` returns the full offset calculated based on the block
    number, offset partition, file system metadata, and sector size provided as input parameters.
    """
    block_size = int(file_system_metadata.block_size)
    fulloffset = block_num * block_size + int(offset_partition) * int(sector_size)
    return fulloffset
