import re
from datetime import datetime
import pytz
import Utility.Other.Terminal_Commands as commando


class Inode:
    '''
    Data class to store Inode information
    '''
    inode_number = 0
    accessed = ""
    file_modified = ""
    inode_modified = ""
    file_created = ""
    blocks = ""
    size = ""

    def __init__(self, inode_number, accessed, file_modified, inode_modified, file_created, blocks, size):
        self.inode_number = inode_number
        self.accessed = accessed
        self.file_modified = file_modified
        self.inode_modified = inode_modified
        self.file_created = file_created
        self.blocks = blocks
        self.size = int(size)
        # print(self.blocks)

    def print(self):
        print(f"Stats for Inode {self.inode_number}")
        print("Accessed: " + self.accessed)
        print("File_modified: " + self.file_modified)
        print("Inode_modified: " + self.inode_modified)
        print("File_created: " + self.file_created)
        print("Direct Blocks: ", self.blocks)
        print("Size: ", self.size)
        print()


text = """
inode: 12
Allocated
Group: 0
Generation Id: 1344355776
uid / gid: 1000 / 1000
mode: rrw-rw-r--
Flags: Extents, 
size: 0
num of links: 1

Inode Times:
Accessed:	2023-09-27 11:52:01.646357931 (CEST)
File Modified:	2023-09-27 11:52:01.646357931 (CEST)
Inode Modified:	2023-09-27 11:52:01.646357931 (CEST)
File Created:	2023-09-27 11:52:01.646357931 (CEST)

Direct Blocks:
"""


def extract_direct_blocks(imagepath, inode_number, offset, verbose=False):
    # TODO unused
    """
    The extract_direct_blocks function takes in an imagepath, an inode number, and a block offset.
    It then uses the istat command to extract the direct blocks from that specific file.
    The function returns a list of all of those direct blocks.
    
    :param imagepath: Specify the path to the image file
    :param inode_number: Specify which inode to look at
    :param offset: Find the inode table
    :param verbose: Print the output of the commando
    :return: A list of the direct blocks
    
    """
    commando.istat(offset, imagepath, inode_number)
    pattern = re.compile(r'Direct Blocks:\s*([\d\s]+)')


def istat_extract_inode(imagepath, inode_number, offset, verbose=False):
    """
    The istat_extract_inode function takes in the path to an image file, an inode number, and a partition offset.
    It then uses the istat command from The Sleuth Kit to extract information about that specific inode.
    The function returns a Inode object containing all of the extracted data.
    
    :param imagepath: Specify the path to the image file
    :param inode_number: Specify the inode number of the file to be extracted
    :param offset: Specify the offset of the partition
    :param verbose: Print the inode information
    :return: An inode object
    
    """
    result = commando.istat(offset, imagepath, inode_number).stdout

    pattern = r"(Accessed:\s*)(.+)|(File Modified:\s*)(.+)|(Inode Modified:\s*)(.+)|(File Created:\s*)(.+)"
    pattern2 = re.compile(r'Direct Blocks:\s*([\d\s]+)')
    pattern3 = re.compile(r'size: (\d+)')

    matches = re.findall(pattern, result)
    Accessed = ""
    File_Modified = ""
    Inode_Modified = ""
    File_Created = ""
    blocks = ""

    for match in matches:
        if match[0]:
            Accessed = match[1]
        elif match[2]:
            File_Modified = match[3]
        elif match[4]:
            Inode_Modified = match[5]
        elif match[6]:
            File_Created = match[7]

    match = pattern2.search(result)
    if match:
        blocks_str = match.group(1)
        # Split the block numbers and convert them to integers
        blocks = [int(block) for block in blocks_str.split()]
    else:
        blocks = None

    match = pattern3.search(result)
    if match:
        size = match.group(1)
    else:
        size = None

    inode = Inode(inode_number, Accessed, File_Modified, Inode_Modified, File_Created, blocks, size)
    if verbose:
        inode.print()
    return inode


def convert_istat_to_timestamp(timestamp_str):
    # Extract the timestamp and timezone information
    """
    The convert_istat_to_timestamp function takes a string of the form
        &quot;YYYY-MM-DD HH:MM:SS.sss (TZ)&quot;
    and returns a datetime object localized to the given timezone TZ.
    
    :param timestamp_str: Extract the timestamp and timezone information
    :return: A datetime object
    
    """
    timestamp_str, tz_str = timestamp_str.split(' (')
    timestamp_str, unused = timestamp_str.split('.')
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    timezone = tz_str[:-1]
    # TODO Buggy workaround
    if timezone == "CEST":
        timezone = "Europe/Berlin"
    # Parse the timezone
    timezone = pytz.timezone(timezone)

    # Localize the timestamp to the given timezone
    localized_timestamp = timezone.localize(timestamp)
    return localized_timestamp
