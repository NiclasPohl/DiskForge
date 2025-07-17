# mmls_extract_all_partitions()
The mmls_extract_all_partitions function takes an imagepath as input and returns a list of PartitionInfo objects.
    The function uses the mmls command to extract information about all partitions in the image. The output from mmls is parsed using regular expressions, and each row is converted into a PartitionInfo object.
## Parameters:
    def mmls_extract_all_partitions(imagepath, verbose=False):
-  imagepath: Specify the path to the image file
-  verbose: Print out the output of the mmls command
- :return: A list of partitioninfo objects

## Workflow:
1. Execute mmls
2. Run regex
3. Create `PartitionInfo` objects