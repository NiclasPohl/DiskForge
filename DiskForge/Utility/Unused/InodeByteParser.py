'''
Inode Parser:
Takes the Byte Information of an Inode an Parses it to the relevant Entries
'''
import mmap
from subprocess import run, PIPE


# All Variables in an Inode:
class Inode:
    i_mode = None
    i_uid = None
    i_size_lo = None
    i_atime = None
    i_ctime = None
    i_mtime = None
    i_dtime = None
    i_gid = None
    i_links_count = None
    i_blocks_lo = None
    i_flags = None
    osd1 = None
    i_block = None
    i_generation = None
    i_file_acl_lo = None
    i_size_high = None
    i_obso_faddr = None
    osd2 = None
    i_extra_isize = None
    i_checksum_hi = None
    i_ctime_extra = None
    i_mtime_extra = None
    i_atime_extra = None
    i_crtime = None
    i_crtime_extra = None
    i_version_hi = None
    i_projid = None

    class Leaf:
        ee_block = None
        ee_block_int = None

        ee_len = None
        ee_len_int = None

        ee_start_hi = None
        ee_start_hi_int = None

        ee_start_lo = None
        ee_start_lo_int = None

        ee_start = None
        ee_start_int = None

        #def __init__(self, ee_block, ee_len, ee_start_hi, ee_start_lo):



    def i_block_parser(self):
        offset = 0

        eh_magic = self.i_block[offset:offset + 2]
        offset += 2

        eh_entries = self.i_block[offset:offset + 2]
        eh_entries_int = int.from_bytes(eh_entries, "little")
        print("eh_entries: " + str(eh_entries_int))
        offset += 2

        eh_max = self.i_block[offset:offset + 2]
        eh_max_int = int.from_bytes(eh_max, "little")
        print("eh_max: " + str(eh_max_int))
        offset += 2

        eh_depth = self.i_block[offset:offset + 2]
        eh_depth_int = int.from_bytes(eh_depth, "little")
        offset += 2
        print("eh_depth: " + str(eh_depth_int))

        eh_generation = self.i_block[offset:offset + 4]
        eh_generation_int = int.from_bytes(eh_generation, "little")
        print("eh_generation: " + str(eh_generation_int))
        offset += 4

        if eh_depth_int == 0:
            print("Leaf")
            for i in range(eh_entries_int):
                ee_block = self.i_block[offset:offset + 4]
                ee_block_int = int.from_bytes(ee_block, "little")
                print("ee_block: " + str(ee_block_int))
                offset += 4
                ee_len = self.i_block[offset:offset + 2]
                ee_len_int = int.from_bytes(ee_len, "little")
                print("ee_len: " + str(ee_len_int))
                offset += 2
                ee_start_hi = self.i_block[offset:offset + 2]
                ee_start_hi_int = int.from_bytes(ee_start_hi, "little")
                print("ee_start_hi:" + str(ee_start_hi_int))
                offset += 2
                ee_start_lo = self.i_block[offset:offset + 4]
                ee_start_lo_int = int.from_bytes(ee_start_lo, "little")
                print("ee_start_lo: " + str(ee_start_lo_int))

                ee_start = ee_start_lo + ee_start_hi # TODO nochmal checken ob das so passt
                ee_start_int = int.from_bytes(ee_start,"little")
                print("ee_start: " + str(ee_start_int))

                offset += 4
        else:
            print("Internal Node")
            for i in range(eh_entries_int):
                ei_block = self.i_block[offset:offset+4]
                offset +=4

                ei_leaf_lo = self.i_block[offset:offset+4]
                offset += 4

                ei_leaf_hi = self.i_block[offset:offset+2]
                offset += 2

                ei_unused = self.i_block[offset:offset+2]
                offset += 2

        # print(magic_number.hex(" "))

    def printInode(self):
        print("i_mode " + str(self.i_mode.hex(" ")))
        print("i_block " + str(self.i_block.hex(" ")))
        self.i_block_parser()

    def __init__(self, i_mode, i_uid, i_size_lo, i_atime, i_ctime, i_mtime, i_dtime, i_gid, i_links_count, i_blocks_lo,
                 i_flags, osd1, i_block, i_generation, i_file_acl_lo, i_size_high,
                 i_obso_faddr, osd2, i_extra_isize, i_checksum_hi, i_ctime_extra, i_mtime_extra, i_atime_extra,
                 i_crtime, i_crtime_extra, i_version_hi, i_projid):
        self.i_mode = i_mode
        self.i_uid = i_uid
        self.i_size_lo = i_size_lo
        self.i_atime = i_atime
        self.i_ctime = i_ctime
        self.i_mtime = i_mtime
        self.i_dtime = i_dtime
        self.i_gid = i_gid
        self.i_links_count = i_links_count
        self.i_blocks_lo = i_blocks_lo
        self.i_flags = i_flags
        self.osd1 = osd1
        self.i_block = i_block
        self.i_generation = i_generation
        self.i_file_acl_lo = i_file_acl_lo
        self.i_size_high = i_size_high
        self.i_obso_faddr = i_obso_faddr
        self.osd2 = osd2
        self.i_extra_isize = i_extra_isize
        self.i_checksum_hi = i_checksum_hi
        self.i_ctime_extra = i_ctime_extra
        self.i_mtime_extra = i_mtime_extra
        self.i_atime_extra = i_atime_extra
        self.i_crtime = i_crtime
        self.i_crtime_extra = i_crtime_extra
        self.i_version_hi = i_version_hi
        self.i_projid = i_projid
        self.printInode()


def get_pagesize():
    command = ['getconf', 'PAGE_SIZE']
    return int(run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True).stdout)


def bytes2inode(address, image_location, verbose=False):
    pagesize = get_pagesize()
    # Offset = ADRESSE//PAGESIZE
    # Index = ADRESSE % PAGESIZE
    # EDGECASE: INDEX + 8 >= PAGESIZE TODO rausfinden ob relevant
    with open(image_location, "r+b") as f:
        usable_offset = address // pagesize * pagesize
        usable_index = address % pagesize
        mm = mmap.mmap(f.fileno(), pagesize, offset=usable_offset)

        offset = usable_index
        i_mode = mm[offset:offset + 2]
        offset += 2

        i_uid = mm[offset:offset + 2]
        offset += 2

        i_size_lo = mm[offset:offset + 4]
        offset += 4

        i_atime = mm[offset:offset + 4]
        offset += 4

        i_ctime = mm[offset:offset + 4]
        offset += 4

        i_mtime = mm[offset:offset + 4]
        offset += 4

        i_dtime = mm[offset:offset + 4]
        offset += 4

        i_gid = mm[offset:offset + 2]
        offset += 2

        i_links_count = mm[offset:offset + 2]
        offset += 2

        i_blocks_lo = mm[offset:offset + 4]
        offset += 4

        i_flags = mm[offset:offset + 4]
        offset += 4

        osd1 = mm[offset:offset + 4]
        offset += 4

        i_block = mm[offset:offset + 60]
        offset += 60

        i_generation = mm[offset:offset + 4]
        offset += 4

        i_file_acl_lo = mm[offset:offset + 4]
        offset += 4

        i_size_high = mm[offset:offset + 4]
        offset += 4

        i_obso_faddr = mm[offset:offset + 4]
        offset += 4

        osd2 = mm[offset:offset + 12]
        offset += 12

        i_extra_isize = mm[offset:offset + 2]
        offset += 2

        i_checksum_hi = mm[offset:offset + 2]
        offset += 2

        i_ctime_extra = mm[offset:offset + 4]
        offset += 4

        i_mtime_extra = mm[offset:offset + 4]
        offset += 4

        i_atime_extra = mm[offset:offset + 4]
        offset += 4

        i_crtime = mm[offset:offset + 4]
        offset += 4

        i_crtime_extra = mm[offset:offset + 4]
        offset += 4

        i_version_hi = mm[offset:offset + 4]
        offset += 4

        i_projid = mm[offset:offset + 4]
        offset += 4

        x = Inode(i_mode, i_uid, i_size_lo, i_atime, i_ctime, i_mtime, i_dtime, i_gid, i_links_count, i_blocks_lo,
                  i_flags,
                  osd1, i_block, i_generation, i_file_acl_lo, i_size_high, i_obso_faddr, osd2, i_extra_isize,
                  i_checksum_hi, i_ctime_extra, i_mtime_extra, i_atime_extra, i_crtime, i_crtime_extra, i_version_hi,
                  i_projid)

        mm.close()
        f.close()
