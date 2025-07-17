import re
import mmap

binary_data = b"\x00\x11\x22\x33\x44\x55\x66\x77"
myfile = "/home/niclas/Utility.img"

with open(myfile, "r+b") as f:
    # Problem Offset muss n*PAGESIZE sein
    # Lösung:
    # Offset = ADRESSE//PAGESIZE
    # Index = ADRESSE % PAGESIZE
    # EDGECASE: INDEX + 8 >= PAGESIZE
    # DANN ÜBERLAUF

    # Offset Inode Access Time 5389056+8 Global gesehen ned nur Partition
    address_Inode = 5389064
    usable_offset = address_Inode//4096*4096
    usable_index = address_Inode % 4096
    print(usable_offset)
    print(usable_index)
    mm = mmap.mmap(f.fileno(), 4096, offset=usable_offset)
    testoutput = mm[usable_index:usable_index+4]
    print(mm[usable_index:usable_index+8].hex())
    new_data = b"\x61\x13\xfb\x41"
    print(new_data)
    #Conversion to little endian
    new_data = new_data[::-1]
    print(new_data.hex())
    mm[usable_index:usable_index+4] = new_data
    print(mm[usable_index:usable_index + 8].hex())
    #mm.close()
    mm.flush()
