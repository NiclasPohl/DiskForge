# extract_values_fsstat()
The extract_values_fsstat function takes in the path to an image file, the offset of a partition within that image
   file, and a boolean value indicating whether or not verbose output is desired. It then uses fsstat to extract 
   information about the file system from that partition. The function returns a FileSystemInformation object containing 
   the extracted information.
## Parameters:
    def extract_values_fsstat(imagepath, offset, verbose=False):
- :param imagepath: Point to the image file on your computer
- :param offset: Tell the function where to start looking for the partition
- :param verbose: Print out the data structure
- :return: A fs_info data structure