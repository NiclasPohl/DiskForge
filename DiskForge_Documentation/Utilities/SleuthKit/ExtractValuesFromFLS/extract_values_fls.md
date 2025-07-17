# extract_values_fls()
The extract_values_fls function takes in the imagepath, offset and searched_file as parameters.
    It then creates a file called Output in the current working directory and runs fls on it with 
    the given parameters. It then iterates through each line of the output file using a regular expression to extract 
    the information from it. The function returns an integer value which is either - 1 or the corresponding inode number for 
    the searched_file.
## Parameters:
    def extract_values_fls(imagepath, offset, searched_file, verbose=False):
-  imagepath: Specify the location of the image file
-  offset: Specify the offset of the partition in question
-  searched_file: Specify the file you want to find inode number for
-  verbose: Print the output of the command to stdout
- :return: The inode number for a given filename
## Workflow:
1. Execute fls
2. Use regex to extract the information