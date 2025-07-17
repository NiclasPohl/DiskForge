import Utility.Other.Terminal_Commands as command
from datetime import datetime

sample_text = """
Group: 0:
  Block Group Flags: [INODE_ZEROED, ]
  Inode Range: 1 - 8192
  Block Range: 0 - 32767
  Layout:
    Super Block: 0 - 0
    Group Descriptor Table: 1 - 4
    Group Descriptor Growth Blocks: 5 - 1028
    Data bitmap: 1029 - 1029
    Inode bitmap: 1045 - 1045
    Inode Table: 1061 - 1572
    Data Blocks: 9253 - 32767
  Free Inodes: 8174 (99%)
  Free Blocks: 1298 (3%)
  Total Directories: 2
  Stored Checksum: 0x89F5

Group: 1:
  Block Group Flags: [INODE_UNINIT, INODE_ZEROED, ]
  Inode Range: 8193 - 16384
  Block Range: 32768 - 65535
  Layout:
    Super Block: 32768 - 32768
    Group Descriptor Table: 32769 - 32772
    Group Descriptor Growth Blocks: 32773 - 33796
    Data bitmap: 1030 - 1030
    Inode bitmap: 1046 - 1046
    Inode Table: 1573 - 2084
    Data Blocks: 33797 - 65535
  Free Inodes: 8192 (100%)
  Free Blocks: 731 (2%)
  Total Directories: 0
  Stored Checksum: 0x2A36
"""

inodes_per_group = 8192

imagefile = ""
imagefile_new = ""
offset = ""


class BlockGroupInfo:
    GroupNumber = ""
    InodeRange = ""

    SuperBlock = ""
    GroupDescriptorTable = ""
    GroupDescriptorGrowthBlocks = ""
    DataBitmap = ""
    InodeBitmap = ""
    InodeTable = ""
    DataBlocks = ""

    highest = -1
    lowest = float("inf")

    def __init__(self, GroupNumber, InodeRange, SuperBlock, GroupDescriptorTable, GroupDescriptorGrowthBlocks,
                 DataBitmap, InodeBitmap, InodeTable, DataBlocks):
        self.GroupNumber = GroupNumber
        #print(f"self.GroupNumber = {self.GroupNumber}")
        self.InodeRange = InodeRange
        #print(f"self.InodeRange = {self.InodeRange}")
        self.SuperBlock = SuperBlock
        if SuperBlock[0] < self.lowest:
            self.lowest = SuperBlock[0]
        if SuperBlock[1] > self.highest:
            self.highest = SuperBlock[1]

        #print(f"self.SuperBlock = {self.SuperBlock}")
        self.GroupDescriptorTable = GroupDescriptorTable
        if SuperBlock[0] < self.lowest:
            self.lowest = SuperBlock[0]
        if SuperBlock[1] > self.highest:
            self.highest = SuperBlock[1]

        #print(f"self.GroupDescriptorTable = {self.GroupDescriptorTable}")
        self.GroupDescriptorGrowthBlocks = GroupDescriptorGrowthBlocks
        if GroupDescriptorGrowthBlocks[0] < self.lowest:
            self.lowest = GroupDescriptorGrowthBlocks[0]
        if GroupDescriptorGrowthBlocks[1] > self.highest:
            self.highest = GroupDescriptorGrowthBlocks[1]

        #print(f"self.GroupDescriptorGrowthBlocks = {self.GroupDescriptorGrowthBlocks}")
        self.DataBitmap = DataBitmap
        if DataBitmap[0] < self.lowest:
            self.lowest = DataBitmap[0]
        if DataBitmap[1] > self.highest:
            self.highest = DataBitmap[1]

        #print(f"self.DataBitmap = {self.DataBitmap}")
        self.InodeBitmap = InodeBitmap
        if InodeBitmap[0] < self.lowest:
            self.lowest = InodeBitmap[0]
        if InodeBitmap[1] > self.highest:
            self.highest = InodeBitmap[1]

        #print(f"self.InodeBitmap = {self.InodeBitmap}")
        self.InodeTable = InodeTable
        if InodeTable[0] < self.lowest:
            self.lowest = InodeTable[0]
        if InodeTable[1] > self.highest:
            self.highest = InodeTable[1]

        #print(f"self.InodeTable = {self.InodeTable}")
        self.DataBlocks = DataBlocks
        if DataBlocks[0] < self.lowest:
            self.lowest = DataBlocks[0]
        if DataBlocks[1] > self.highest:
            self.highest = DataBlocks[1]
        #print(f"self.DataBlocks = {self.DataBlocks}")

    def isIn(self, blocknumber,imagefile_base,imagefile_new,offset):
        #global start_time
        #print(f"Time to reach isIn{datetime.now()-start_time}")
        if blocknumber < self.lowest or blocknumber > self.highest:
            return -1
        #print(f"Time First Check{datetime.now() - start_time}")
        if blocknumber >= self.SuperBlock[0] and blocknumber <= self.SuperBlock[1]:
            #print(f"Time Second Check (in){datetime.now() - start_time}")
            return f"Block {blocknumber} is Superblock of Group {self.GroupNumber}"
        #print(f"Time Second Check (out){datetime.now() - start_time}")
        if blocknumber >= self.GroupDescriptorTable[0] and blocknumber <= self.GroupDescriptorTable[1]:
            #print(f"Time Third Check(in){datetime.now() - start_time}")
            return f"Block {blocknumber} is Group Descriptor Table Block Number {blocknumber - self.GroupDescriptorTable[0]} of Group {self.GroupNumber}"
        #print(f"Time Third Check(out){datetime.now() - start_time}")
        if blocknumber >= self.GroupDescriptorGrowthBlocks[0] and blocknumber <= self.GroupDescriptorGrowthBlocks[1]:
            return f"Block {blocknumber} is Group Descriptor Growth Block Number {blocknumber - self.GroupDescriptorGrowthBlocks[0]} of Group {self.GroupNumber}"
        if blocknumber >= self.DataBitmap[0] and blocknumber <= self.DataBitmap[1]:
            return f"Block {blocknumber} is Data Bitmap of Group {self.GroupNumber}"
        if blocknumber >= self.InodeBitmap[0] and blocknumber <= self.InodeBitmap[1]:
            return f"Block {blocknumber} is Data Bitmap of Group {self.GroupNumber}"
        if blocknumber >= self.InodeTable[0] and blocknumber <= self.InodeTable[1]:
            return (
                f"Block {blocknumber} is Inode Table Block Number {blocknumber - self.InodeTable[0]} of Group {self.GroupNumber}\n"
                f"      It holds inode numbers {self.InodeRange[0] + 16 * (blocknumber - self.InodeTable[0])} till {self.InodeRange[0] + 16 * (blocknumber - self.InodeTable[0] + 1) - 1}\n"
                f"      Inodes changed {istat_diff(self.InodeRange[0] + 16 * (blocknumber - self.InodeTable[0]),self.InodeRange[0] + 16 * (blocknumber - self.InodeTable[0] + 1) - 1,imagefile_base,imagefile_new,offset)}")
        if blocknumber >= self.DataBlocks[0] and blocknumber <= self.DataBlocks[1]:
            return (f"Block {blocknumber} is Data Block of Group {self.GroupNumber}\n"
                    f"      Old: It is used by Inode {command.ifind(blocknumber=blocknumber, imagefile=imagefile_base, offset=offset)}\n"
                    f"      New: It is used by Inode {command.ifind(blocknumber=blocknumber, imagefile=imagefile_new, offset=offset)}")
        return -1


buf = sample_text.split("\n")

block_groups = []

x = 0

GroupNumber = -1
InodeRange = (-1, -1)

SuperBlock = (-1, -1)
GroupDescriptorTable = (-1, -1)
GroupDescriptorGrowthBlocks = (-1, -1)
DataBitmap = (-1, -1)
InodeBitmap = (-1, -1)
InodeTable = (-1, -1)
DataBlocks = (-1, -1)

def istat_diff(start_inode,end_inode,imagefile_old,imagefile_new,offset):
    res = []
    check_inode = start_inode
    while check_inode <= end_inode:
        a = command.istat(offset=offset,imagepath=imagefile_old,inodenumber=check_inode).stdout
        b = command.istat(offset=offset,imagepath=imagefile_new,inodenumber=check_inode).stdout
        if a != b:
            res.append(check_inode)
        check_inode += 1
    return res

def split_Group(x):
    a = x.split(" ")
    a = a[1].split(":")
    a = int(a[0])
    return a


def split_Val(x):
    x = x.split("-")
    a = x[0].split(" ")
    b = x[1].split(" ")
    b = int(b[1])
    a = int(a[len(a) - 2])
    res = (a, b)
    return res

imagefile_base = "/media/niclas/Crucial X6/asservat_73382-23/asservat_74382-23.img"
offset = 1054720
def parse_fsstat(imagefile_base,offset):
    GroupNumber = -1
    InodeRange = (-1, -1)

    SuperBlock = (-1, -1)
    GroupDescriptorTable = (-1, -1)
    GroupDescriptorGrowthBlocks = (-1, -1)
    DataBitmap = (-1, -1)
    InodeBitmap = (-1, -1)
    InodeTable = (-1, -1)
    DataBlocks = (-1, -1)
    buf = command.fsstat(offset,imagefile_base).stdout
    buf = buf.split("\n")
    for i in range(len(buf)):
        if (buf[i].__contains__("Group:") and not buf[i].__contains__("Flex")):  # Start of new block
            if(GroupNumber==-1):
                GroupNumber = split_Group(buf[i])
            else:
                x = BlockGroupInfo(GroupNumber, InodeRange, SuperBlock, GroupDescriptorTable, GroupDescriptorGrowthBlocks,
                                   DataBitmap, InodeBitmap, InodeTable, DataBlocks)
                block_groups.append(x)
                GroupNumber = split_Group(buf[i])
                InodeRange = (-1, -1)
                SuperBlock = (-1, -1)
                GroupDescriptorTable = (-1, -1)
                GroupDescriptorGrowthBlocks = (-1, -1)
                DataBitmap = (-1, -1)
                InodeBitmap = (-1, -1)
                InodeTable = (-1, -1)
                DataBlocks = (-1, -1)
        elif (buf[i].__contains__("Inode Range:")):
            InodeRange = split_Val(buf[i])
        elif (buf[i].__contains__("Super Block:")):
            SuperBlock = split_Val(buf[i])
        elif (buf[i].__contains__("Group Descriptor Table:")):
            GroupDescriptorTable = split_Val(buf[i])
        elif (buf[i].__contains__("Group Descriptor Growth Blocks:")):
            GroupDescriptorGrowthBlocks = split_Val(buf[i])
        elif (buf[i].__contains__("Data bitmap:")):
            DataBitmap = split_Val(buf[i])
        elif (buf[i].__contains__("Inode bitmap:")):
            InodeBitmap = split_Val(buf[i])
        elif (buf[i].__contains__("Inode Table:")):
            InodeTable = split_Val(buf[i])
        elif (buf[i].__contains__("Data Blocks:")):
            DataBlocks = split_Val(buf[i])
    x = BlockGroupInfo(GroupNumber, InodeRange, SuperBlock, GroupDescriptorTable, GroupDescriptorGrowthBlocks,
                       DataBitmap, InodeBitmap, InodeTable, DataBlocks)
    block_groups.append(x)
start_time = 0
def find_data(imagefile_base,imagefile_new,offset,blocks):
    global start_time
    parse_fsstat(imagefile_base, offset)
    res = []
    j = 0
    start_index = 0
    len_block = len(block_groups)
    start_time = datetime.now()
    for block in blocks:
        print(f"Time to reach block {j}: {datetime.now()-start_time}")
        start_time = datetime.now()
        print(f"{j/len_block*100}%")
        j = j+1
        start_val = int(start_index)
        found = False
        for i in range(start_val,len_block):
            #print(i)
            #print(f"Time To reach block lookup: {datetime.now()-start_time}")
            #start_time = datetime.now()
            x = block_groups[i].isIn(block,imagefile_base,imagefile_new,offset)
            #print(f"Block Check{datetime.now()-start_time}")
            #start_time = datetime.now()
            if not x == -1:
                if start_index < i:
                    start_index += 0.9
                else:
                    start_index -= 0.05
                #print(f"Start Index = {start_index}")
                #print(f"First {i} vs {start_index}")
                #print(f"Time To reach append: {datetime.now() - start_time}")
                #start_time = datetime.now()
                res.append(x)
                #print(f"Time To append: {datetime.now() - start_time}")
                #start_time = datetime.now()
                found = True
                break
        if not found:
            for i in range(len_block):
                x = block_groups[i].isIn(block, imagefile_base, imagefile_new, offset)
                if not x == -1:
                    start_index = (3 * start_index + i) / 4
                    #print(f"Second {i} vs {start_val}")
                    res.append(x)
                    found = True
                    break
    return res

