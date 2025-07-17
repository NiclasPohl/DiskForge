# Metadata - Delta Shift
The Delta Shift module for the inode metadata in the in the file [Meta_DeltaShift.py](https://faui1-gitlab.cs.fau.de/lena.voigt/diskforge/-/blob/main/DiskForge/Modules/Timestomping/LogFiles/Log_DeltaShift.py).

It contains the function *Meta_DeltaShift* which uses the following parameters:
- image_location: Location of the disk image
- file_location: location of the file that should be modified
- partition_num: Partition Number
- verbose: Increase Verbosity
- args: Arguments used to call this function
- shift_type: What unit should be shifted
- shift_num: How much of that unit should be shifted

Workflow:
1. Extract Inode Number Corresponding to Filename
2. Calculate Inode Offset
3. Shift timestamp
4. Update crc32c checksum