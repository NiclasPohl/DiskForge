# read_generation()
This Python function reads 4 bytes of generation data from a disk image at a specified offset position.
## Parameters:
    def read_generation(total_offset, disk_image):
- total_offset: The `total_offset` parameter represents the starting offset on the disk where
    the data is located. It is the cumulative offset that includes any initial offset before reaching
    the specific data of interest
- disk_image: The `disk_image` parameter is the path to the disk image file from which you want
    to read the generation data. This function reads 4 bytes of data starting from the position
    calculated by adding the `total_offset` and 100, within the specified disk image file
- **return:** The function `read_generation` reads 4 bytes of data from the disk image starting at the
    position calculated by adding 100 to the `total_offset` provided as an argument. It returns the
    generation data read from the disk image as a bytes object.
    """

## Workflow:
1. Open disk image at correct position
2. Read data