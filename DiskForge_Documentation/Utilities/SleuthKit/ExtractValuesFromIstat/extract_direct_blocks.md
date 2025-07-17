# extract_direct_blocks()
The extract_direct_blocks function takes in an imagepath, an inode number, and a block offset.
    It then uses the istat command to extract the direct blocks from that specific file.
    The function returns a list of all of those direct blocks.
## Parameters:
    def extract_direct_blocks(imagepath, inode_number, offset, verbose=False):
-  imagepath: Specify the path to the image file
-  inode_number: Specify which inode to look at
-  offset: Find the inode table
-  verbose: Print the output of the commando
- :return: A list of the direct blocks
## Workflow:
-- Unused