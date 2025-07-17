import re
import Utility.Other.Terminal_Commands as commando

# Sample text
sample_text = """
FILE SYSTEM INFORMATION
--------------------------------------------
File System Type: Ext4
Volume Name: MASTER
Volume ID: 5c2cba37c927d2a613497c222a1472cb

Last Written at: 2023-09-27 13:54:27 (CEST)
Last Checked at: 2023-09-27 13:54:16 (CEST)

Last Mounted at: 2023-09-27 11:53:15 (CEST)
Unmounted properly
Last mounted on: /media/niclas/MASTER

Source OS: Linux
Dynamic Structure
Compat Features: Journal, Ext Attributes, Resize Inode, Dir Index
InCompat Features: Filetype, Extents, 64bit, Flexible Block Groups, 
Read Only Compat Features: Sparse Super, Large File, Huge File, Extra Inode Size

Journal ID: 00
Journal Inode: 8

METADATA INFORMATION
--------------------------------------------
Inode Range: 1 - 8145
Root Directory: 2
Free Inodes: 8128
Inode Size: 256

CONTENT INFORMATION
--------------------------------------------
Block Groups Per Flex Group: 16
Block Range: 0 - 30975
Block Size: 4096
Free Blocks: 13049

BLOCK GROUP INFORMATION
--------------------------------------------
Number of Block Groups: 2
Inodes per group: 8144
Blocks per group: 32768

Group: 0:
  Block Group Flags: [INODE_ZEROED] 
  Inode Range: 1 - 8144
  Block Range: 0 - 30975
  Layout:
    Super Block: 0 - 0
    Group Descriptor Table: 1 - 1
    Group Descriptor Growth Blocks: 2 - 1025
    Data bitmap: 1027 - 1027
    Inode bitmap: 1043 - 1043
    Inode Table: 1059 - 1567
    Uninit Data Bitmaps: 1027 - 1042
    Uninit Inode Bitmaps: 1043 - 1058
    Uninit Inode Table: 1059 - 9202
    Data Blocks: 9202 - 30975
  Free Inodes: 8128 (99%)
  Free Blocks: 13049 (42%)
  Total Directories: 2
  Stored Checksum: 0xD74B

Group: 2:
  Block Group Flags: [INODE_ZEROED] 
  Inode Range: 8145 - 16288
  Block Range: 30976 - 61951
  Layout:
    Super Block: 0 - 0
    Group Descriptor Table: 1 - 1
    Group Descriptor Growth Blocks: 2 - 1025
    Data bitmap: 1027 - 1027
    Inode bitmap: 1043 - 1043
    Inode Table: 1064 - 1567
    Uninit Data Bitmaps: 1027 - 1042
    Uninit Inode Bitmaps: 1043 - 1058
    Uninit Inode Table: 1059 - 9202
    Data Blocks: 9202 - 30975
  Free Inodes: 8128 (99%)
  Free Blocks: 13049 (42%)
  Total Directories: 2
  Stored Checksum: 0xD74B

Group: 3:
  Block Group Flags: [INODE_ZEROED] 
  Inode Range: 8145 - 16288
  Block Range: 30976 - 61951
  Layout:
    Super Block: 0 - 0
    Group Descriptor Table: 1 - 1
    Group Descriptor Growth Blocks: 2 - 1025
    Data bitmap: 1027 - 1027
    Inode bitmap: 1043 - 1043
    Inode Table: 1064 - 1567
    Uninit Data Bitmaps: 1027 - 1042
    Uninit Inode Bitmaps: 1043 - 1058
    Uninit Inode Table: 1059 - 9202
    Data Blocks: 9202 - 30975
  Free Inodes: 8128 (99%)
  Free Blocks: 13049 (42%)
  Total Directories: 2
  Stored Checksum: 0xD74B
"""


class FileSystemInformation:
    '''
    Data structure to store the output of fsstat
    '''
    inode_size = ""
    block_size = ""
    inode_tables = []
    inodes_per_group = ""
    blocks_per_group = ""

    def __init__(self, inode_size, block_size, inode_tables, inodes_per_group, blocks_per_group):
        """
        The __init__ function is called when the class is instantiated.
        It sets up all of the variables that are needed for this class to function properly.
        
        :param self: Represent the instance of the class
        :param inode_size: Store the size of each inode
        :param block_size: Determine the size of each block in bytes
        :param inode_tables: Store the number of inode tables per group
        :param inodes_per_group: Determine the number of inodes per group
        :param blocks_per_group: Determine how many blocks are in each group
        :return: The object instance
        
        """
        self.inode_size = inode_size
        self.block_size = block_size
        self.inode_tables = inode_tables
        self.inodes_per_group = inodes_per_group
        self.blocks_per_group = blocks_per_group

    def print(self):
        """
        The print function prints the following information:
            Inode Size: The size of each inode.
            Block Size: The size of each block.
            Inodes per Group: How many inodes are contained within a group.
            Blocks per Group: How many blocks are contained within a group.
        
        :param self: Represent the instance of the class
        :return: Nothing
        
        """
        print("\nInode Size: " + self.inode_size)
        print("Block Size: " + self.block_size)
        print("Inodes per Group: " + self.inodes_per_group)
        print("Blocks per Group: " + self.blocks_per_group)
        for i in range(len(self.inode_tables)):
            print("Group: " + self.inode_tables[i].group + ", Inode: " + self.inode_tables[i].start)


class InodeTables:
    '''
    Data structure to store the Inode Table information we need
    '''
    start = ""
    group = ""

    def __init__(self, start, group):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines what attributes it has.
        In this case, we are setting up a new object with two attributes: start and group.
        
        :param self: Represent the instance of the object itself
        :param start: Set the starting position of the sprite
        :param group: Determine what group the player is in
        :return: An object
        
        """
        self.start = start
        self.group = group


def extract_values_fsstat(imagepath, offset, verbose=False):
    """
    The extract_values_fsstat function takes in the path to an image file, the offset of a partition within that image
    file, and a boolean value indicating whether or not verbose output is desired. It then uses fsstat to extract
    information about the file system from that partition. The function returns a FileSystemInformation object containing
    the extracted information.

    :param imagepath: Point to the image file on your computer
    :param offset: Tell the function where to start looking for the partition
    :param verbose: Print out the data structure
    :return: A fs_info data structure

    """
    result = commando.fsstat(offset, imagepath)
    fsstat_output = result.stdout

    '''
    These are the patterns we need to extract the important data
    '''
    patterns = {
        "Inode Size": r"Inode Size: (\d+)",
        "Block Size": r"Block Size: (\d+)",
        "Inode Table": r"Group: (\d+):\n(?:.|\n)+?Inode Table: (\d+)",
        "Inodes per group": r"Inodes per group: (\d+)",
        "Blocks per group": r"Blocks per group: (\d+)"
    }

    '''
    Empty data  structure
    '''
    group_inode_pairs = []

    '''
    Find all Inode Tables
    '''
    inode_table_matches = re.findall(patterns["Inode Table"], fsstat_output)
    for match in inode_table_matches:
        group_number, inode_number = match
        group_inode_pairs.append((group_number, inode_number))

    '''
    Extract other patterns
    '''
    extracted_values = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, fsstat_output)
        if match:
            extracted_values[key] = match.group(1)

    '''
    Gernerate the Inode Tables Data
    '''
    inode_tables = []
    for group, inode in group_inode_pairs:
        table = InodeTables(start=inode, group=group)
        inode_tables.append(table)

    '''
    Map the data
    '''
    for key, value in extracted_values.items():
        match key:
            case "Inode Size":
                inode_size = value
            case "Block Size":
                block_size = value
            case "Inodes per group":
                inodes_per_group = value
            case "Blocks per group":
                blocks_per_group = value

    fs_info = FileSystemInformation(inode_size=inode_size, block_size=block_size, inodes_per_group=inodes_per_group,
                                    blocks_per_group=blocks_per_group, inode_tables=inode_tables)

    return fs_info
