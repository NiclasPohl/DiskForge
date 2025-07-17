from subprocess import run, PIPE
from TimeModTool import fsstat_parser2_0

image = "/media/niclas/Crucial X6/asservat_73382-23/asservat_74382-23.img"

image2 = "/media/niclas/Crucial X6/ManipulatedDiskImages/Metadata/Touch/asservat_74382-23_meta_touch.img"

filename = "/media/niclas/Crucial X6/ManipulatedDiskImages/Metadata/Touch/cmp_meta_touch"

detailed = False

results = []
bytes_nums = []
blocks = []

offset = 1054720

blocksize = 4096
startbyte = 1054720*512

file1 = open(filename, 'r')
Lines = file1.readlines()

for Line in Lines:
    bytes_nums.append(int(Line[0:11])-1)

curStart = bytes_nums[0]
curEnd = 0

outputfile = filename + "_parsed_cool"

for i in range(len(bytes_nums)):
    if(i+1==len(bytes_nums)):
        curEnd = bytes_nums[i]
        results.append((curStart,curEnd))
        break
    if not bytes_nums[i] + 1 == bytes_nums[i+1]:
        curEnd = bytes_nums[i]
        results.append((curStart,curEnd))
        curStart = bytes_nums[i+1]

with open(outputfile,"a") as f:
    print(f"How many Bytes have been changed: {len(bytes_nums)}",file = f)
    if detailed:
        for i in range(len(results)):
            print(f"From Byte {results[i][0]} till {results[i][1]}",file = f)

    print("",file = f)

    lastblock = ""

    for i in range(len(bytes_nums)):
        currblock = (bytes_nums[i]-startbyte)//blocksize
        if i == 0:
            lastblock = currblock
            blocks.append(currblock)
        if not currblock == lastblock:
            lastblock = currblock
            blocks.append(currblock)

    print(f"How many Blocks have been changed: {len(blocks)}",file = f)
    print("Block Numbers:",file = f)
    print(blocks,file = f)

    block_ranges = []

    begin_block = -1
    last_block = -1
    for i in range(len(blocks)):
        if i == 0:
            begin_block = blocks[i]
            last_block = blocks[i]
            continue
        else:
            if last_block + 1 == blocks[i]:
                last_block = blocks[i]
            else:
                block_ranges.append((begin_block,last_block))
                begin_block = blocks[i]
                last_block = blocks[i]
    block_ranges.append((begin_block,last_block))
    print("Block Ranges:", file = f)
    print(block_ranges,file=f)

    blocks_parsed = fsstat_parser2_0.find_data(imagefile_base=image,imagefile_new=image2,offset=offset,blocks=blocks)
    for blocki in blocks_parsed:
        print(blocki,file = f)

    def command1(i):
        command = f"blkstat -o {offset} {image} {i}"
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        if not result.stderr == "":
            print(result.stderr)
        result = result.stdout
        return result

    def command2(i):
        command = f"ifind -o {offset} -d {i} {image}"
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        if not result.stderr == "":
            print(result.stderr)
        result = result.stdout
        return result

    def command3(i):
        command = f"blkstat -o {offset} {image2} {i}"
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        if not result.stderr == "":
            print(result.stderr)
        result = result.stdout
        return result

    def command4(i):
        command = f"ifind -o {offset} -d {i} {image2}"
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        if not result.stderr == "":
            print(result.stderr)
        result = result.stdout
        return result
    if False:
        for block in blocks:
            print(block)
            stat = command1(block)
            inode = command2(block)
            print(f"In Base Image Block Number {block} resides in {stat} and is used by {inode}",file = f)
            stat = command3(block)
            inode = command4(block)
            print(f"In Modified Image Block Number {block} resides in {stat} and is used by {inode}", file=f)