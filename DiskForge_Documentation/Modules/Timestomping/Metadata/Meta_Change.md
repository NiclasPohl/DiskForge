# Metadtata - Change

The Change module for the inode metadata in the in the file *[Meta_Change.py](https://faui1-gitlab.cs.fau.de/lena.voigt/diskforge/-/blob/main/DiskForge/Modules/Timestomping/Metadata/Meta_Change.py)*.

It contains the function *Meta_Change* which uses the following parameters:
- image_location: Location of the disk image
- file_location: location of the file that should be modified
- partition_num: Partition Number
- verbose: Increase Verbosity
- args: Arguments used to call this function
- timestamp: What timestamp should be altered
- nts: New Timestamp

Workflow:
1. Extract Inode Number Corresponding to Filename
2. Calculate Inode Offset
3. Update timestamp
4. Update crc32c checksum