# read_uuid()
This Python function reads a UUID from a specified offset within a disk image file.
## Parameters:
    def read_uuid(offset_partition, disk_image):
- offset_partition: The `offset_partition` parameter represents the starting offset of the
    partition within the disk image from which you want to read the UUID. This offset is typically
    specified in bytes
- disk_image: The `disk_image` parameter in the `read_uuid` function is the path to the disk
    image file from which you want to read the UUID. Make sure to provide the full path to the disk
    image file when calling this function
- **return:** The function `read_uuid` reads a UUID (Universally Unique Identifier) from a disk image
    file at a specific offset. It skips over a buffer in Block 0 and then jumps to the UUID field to
    read 16 bytes (128 bits) of data. The function returns the UUID as a bytes object.
## Workflow:
1. Calculate offset of superblock
2. Open File at superblock position
3. Read UUID