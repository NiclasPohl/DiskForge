import crc32c
import binascii
import zlib
import hashlib

"""
    The provided Python script contains functions to read and manipulate inode data, UUID, superblock
    data, and compute CRC32C checksum for serialized inode data in a disk image file.
"""


def read_inode(full_offset, disk_image):
    """
    The `read_inode` function reads inode data from a disk image file, inserts zero bytes at specific
    positions, and returns the modified inode data.
    
    :param full_offset: The `full_offset` parameter in the `read_inode` function represents the position
    of the inode on the disk image. It is the offset at which the inode data starts within the disk
    image file. This offset is used to locate and read the specific inode data from the disk image file
    :param disk_image: The `disk_image` parameter in the `read_inode` function is the path to the disk
    image file from which the inode data will be read. This file is assumed to contain the data
    representing the disk's contents, including the inodes. The function opens this file in binary mode
    ('rb')
    :return: The function `read_inode` reads inode data from a disk image file at a specified offset. It
    reads a total of 256 bytes of data from the disk image file starting at the given offset. The
    function then inserts zero bytes at specific positions within the inode data before returning the
    modified inode data as a bytes object.
    """
    # Read the inode data from disk
    # For demonstration purposes, let's assume inode data is read from a file
    with open(disk_image, 'rb') as f:
        # Seek to the position of the inode on disk
        f.seek(full_offset)
        # Read the inode data (assuming inode_size bytes per inode)
        inode_data = f.read(124)

        # Insert Zero Bytes at the place of the Checksum field
        inode_data = inode_data + bytes(2)
        f.seek(full_offset + 126)
        inode_data = inode_data + f.read(4)

        # Insert Zero Bytes at the place of the Checksum field
        inode_data = inode_data + bytes(2)

        f.seek(full_offset + 132)
        inode_data = inode_data + f.read(256 - 132)
    return inode_data


def read_uuid(offset_partition, disk_image):
    """
    This Python function reads a UUID from a specified offset within a disk image file.
    
    :param offset_partition: The `offset_partition` parameter represents the starting offset of the
    partition within the disk image from which you want to read the UUID. This offset is typically
    specified in bytes
    :param disk_image: The `disk_image` parameter in the `read_uuid` function is the path to the disk
    image file from which you want to read the UUID. Make sure to provide the full path to the disk
    image file when calling this function
    :return: The function `read_uuid` reads a UUID (Universally Unique Identifier) from a disk image
    file at a specific offset. It skips over a buffer in Block 0 and then jumps to the UUID field to
    read 16 bytes (128 bits) of data. The function returns the UUID as a bytes object.
    """
    # Skips over Buffer in Block 0 and then jumps to UUID field
    total_offset = offset_partition + 1024 + 104
    with open(disk_image, 'rb') as f:
        f.seek(total_offset)
        uuid = f.read(16)
    return uuid


def read_superblock(offset_partition, disk_image):
    """
    The function `read_superblock` reads and returns the superblock data from a disk image starting at a
    specified offset within a partition.
    
    :param offset_partition: The `offset_partition` parameter in the `read_superblock` function
    represents the starting offset of the partition within the disk image where the superblock is
    located. This offset is used to calculate the total offset to jump to the superblock within the disk
    image
    :param disk_image: The `disk_image` parameter refers to the path of the disk image file from which
    you want to read the superblock. This file contains the binary data representing the disk's
    contents, including the superblock information. You need to provide the full path to the disk image
    file as a string when calling
    :return: The function `read_superblock` returns the superblock data read from the disk image
    starting at the specified offset. The superblock data is read as a binary string of length 1020
    bytes.
    """
    # Jumps to Superblock
    total_offset = offset_partition + 1024
    with open(disk_image, 'rb') as f:
        f.seek(total_offset)
        superblock = f.read(1020)
    return superblock


def read_generation(total_offset, disk_image):
    """
    This Python function reads 4 bytes of generation data from a disk image at a specified offset
    position.
    
    :param total_offset: The `total_offset` parameter represents the starting offset on the disk where
    the data is located. It is the cumulative offset that includes any initial offset before reaching
    the specific data of interest
    :param disk_image: The `disk_image` parameter is the path to the disk image file from which you want
    to read the generation data. This function reads 4 bytes of data starting from the position
    calculated by adding the `total_offset` and 100, within the specified disk image file
    :return: The function `read_generation` reads 4 bytes of data from the disk image starting at the
    position calculated by adding 100 to the `total_offset` provided as an argument. It returns the
    generation data read from the disk image as a bytes object.
    """
    with open(disk_image, 'rb') as f:
        # Seek to the position of the inode on disk
        full_offset = total_offset + 100

        f.seek(full_offset)
        # Read the generation data
        generation_data = f.read(4)
    return generation_data


def serialize_inode(inode_data, inode_number, filesystem_uuid, generation):
    """
    The function `serialize_inode` takes inode data, inode number, filesystem UUID, and generation as
    input, and returns a serialized inode.
    
    :param inode_data: The `inode_data` parameter typically contains information about a file or
    directory, such as permissions, timestamps, size, and pointers to data blocks. It is the actual data
    associated with an inode in a filesystem
    :param inode_number: The `inode_number` parameter represents the unique identifier of an inode
    within a filesystem. It is typically an integer value that identifies a specific inode within the
    filesystem
    :param filesystem_uuid: A filesystem_uuid is a unique identifier assigned to a file system. It is
    used to distinguish one file system from another
    :param generation: Generation typically refers to the version number or timestamp associated with a
    particular piece of data. In the context of file systems, it is often used to track changes to a
    file or directory. It helps in ensuring data consistency and integrity
    :return: The function `serialize_inode` returns the serialized inode data, which is a combination of
    the filesystem UUID, inode number, generation, and inode data.
    """
    serialized_inode = filesystem_uuid + inode_number.to_bytes(4, byteorder='little') + generation + inode_data
    return serialized_inode


def read_seed():
    # Not Implemented
    return 0


def convert_crc32c(crc32c_val):
    """
    The function `convert_crc32c` takes a CRC32C value, inverts it, converts it to a bytearray, and then
    reverses the order of the bytes before returning the result.
    
    :param crc32c_val: It looks like the code you provided is attempting to convert a CRC32C value.
    However, there seems to be an issue with the conversion process. Before I can proceed, could you
    please provide the value of `crc32c_val` that you would like to convert?
    :return: The function `convert_crc32c` returns a bytearray that represents the converted CRC32C
    value after inverting and reversing the input CRC32C value.
    """
    inverter = 0xFFFFFFFF
    inverted_crc32c = inverter - crc32c_val
    inverted_crc32c = hex(inverted_crc32c)
    inverted_crc32c = inverted_crc32c[2:]
    if len(inverted_crc32c) % 2 != 0:
        inverted_crc32c = '0' + inverted_crc32c
    converted_crc32c = bytearray.fromhex(inverted_crc32c)
    converted_crc32c.reverse()
    return converted_crc32c


def compute_inode_crc32c(inode_number, offset_partition, offset_inode, disk_image):
    """
    The function `compute_inode_crc32c` reads inode data from a disk image, serializes it with inode
    number and filesystem UUID, and computes a CRC32C checksum.
    
    :param inode_number: The `inode_number` parameter is the unique identifier for an inode in a
    filesystem. It is used to locate and access specific metadata information about a file or directory
    stored on the disk
    :param offset_partition: The `offset_partition` parameter typically refers to the starting offset of
    a partition within a disk image. This offset is used to locate the specific partition on the disk
    image where the file system is stored. It is important for reading data related to the file system,
    such as the UUID (Universally Unique
    :param offset_inode: The `offset_inode` parameter typically refers to the location of the inode
    within the disk image. It is the offset value that points to the starting position of the inode data
    on the disk. This value is used to locate and read the inode data from the disk image
    :param disk_image: The `disk_image` parameter in the `compute_inode_crc32c` function is typically a
    binary representation of the disk or partition from which you are reading the inode data. It could
    be a file containing the raw data of the disk or partition, allowing you to read specific sectors or
    blocks to extract
    :return: The function `compute_inode_crc32c` returns the CRC32C checksum computed for the serialized
    inode data along with the inode number and filesystem UUID.
    """
    # Read inode data from disk
    inode_data = read_inode(offset_inode, disk_image)
    generation_data = read_generation(offset_inode, disk_image)
    # print("Gen Data {}".format(generation_data))
    filesystem_uuid = read_uuid(offset_partition, disk_image)
    print(binascii.hexlify(filesystem_uuid))
    # Serialize inode data along with inode number and filesystem UUID
    serialized_inode = serialize_inode(inode_data, inode_number, filesystem_uuid, generation_data)
    # Compute CRC32C checksum
    crc32c_checksum = convert_crc32c(crc32c.crc32c(serialized_inode))
    return crc32c_checksum


# Example usage
if False:
    inode_number = 1311789
    offset_partition = 1054720 * 512
    disk_image = "/media/niclas/Crucial X6/asservat_73382-23/asservat_74382-23.img"
    offset_inode = 22015257600

    crc32c2 = compute_inode_crc32c(inode_number, offset_partition, offset_inode, disk_image)
    print("CRC32C checksum for inode {}: {}".format(inode_number, binascii.hexlify(crc32c2)))
