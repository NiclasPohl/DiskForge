# extract_all_inodes()
The extract_all_inodes function takes in the path to an image file and the offset of a partition within that image
    file. It then uses fls to extract all of the inodes from that partition, returning them as a list.
## Parameters:
    def extract_all_inodes(imagepath, offset):
-  imagepath: Specify the path to the image file on your computer
-  offset: Specify the offset of the partition
- :return: A list of all inodes
## Workflow:
1. Execute fls
2. For each line of the output
3. Regex match for inode number and file name