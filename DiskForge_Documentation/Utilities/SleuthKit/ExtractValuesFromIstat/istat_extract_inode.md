# istat_extract_inode()
The istat_extract_inode function takes in the path to an image file, an inode number, and a partition offset.
    It then uses the istat command from The Sleuth Kit to extract information about that specific inode.
    The function returns a Inode object containing all of the extracted data.
## Parameters:
    def istat_extract_inode(imagepath, inode_number, offset, verbose=False):
-  imagepath: Specify the path to the image file
-  inode_number: Specify the inode number of the file to be extracted
-  offset: Specify the offset of the partition
-  verbose: Print the inode information
- :return: An inode object
## Workflow:
1. Execute istat
2. Run regex on output
3. Create Inode object