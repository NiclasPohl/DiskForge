import re
import os

from Utility.File_Operations.OpenFiles import openFile
from Utility.Other.WriteTimeModLog import writeStderr

import Utility.Other.Terminal_Commands as commando

# Sample text
sample_text = """d/d 11:    lost+found
r/r 12:    TestFile1
r/r 13:    TestFile2
r/r 14:    TestFile3
r/r 15:    TestFile4
r/r 16:    TestFile5
V/V 8145:  $OrphanFiles
custom_string 789:  CustomFile"""

''' OLD VERSION
def extract_values_fls(imagepath, offset, searched_file, verbose=False):
    # Running on sample values for now
    # imagepath = "/home/niclas/MasterThesisTest.img"
    # offset = "2048"
    # searched_file = "TestFile1"

    command = ['fls', '-p', '-r', '-o', offset, imagepath]
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    fls_output = result.stdout
    # Initialize an empty dictionary to store the mapping
    inode_mapping = {}

    # Iterate through the lines using a flexible regular expression to extract the information
    lines = fls_output.split('\n')
    for line in lines:
        match = re.search(r'[^:]+ (\d+):[ \t]+(.+)', line)
        if match:
            inode = int(match.group(1))
            filename = match.group(2)
            inode_mapping[filename] = inode

    # Function to get the inode number for a given filename
    def get_inode_number(filename):
        return inode_mapping.get(filename, None)

    # Example usage:
    inode_number = get_inode_number(searched_file)

    if inode_number is not None:
        if verbose:
            print(f"\nThe corresponding inode number for {searched_file} is {inode_number}")
        return inode_number
    else:
        if verbose:
            print(f"Filename {searched_file} not found in the mapping.")
        return -1
    '''


def extract_values_fls(imagepath, offset, searched_file, verbose=False):
    """
    The extract_values_fls function takes in the imagepath, offset and searched_file as parameters.
    It then creates a file called Output in the current working directory and runs fls on it with 
    the given parameters. It then iterates through each line of the output file using a regular expression to extract 
    the information from it. The function returns an integer value which is either - 1 or the corresponding inode number for 
    the searched_file.
    
    :param imagepath: Specify the location of the image file
    :param offset: Specify the offset of the partition in question
    :param searched_file: Specify the file you want to find inode number for
    :param verbose: Print the output of the command to stdout
    :return: The inode number for a given filename
    
    """
    current_working_directory = os.getcwd()
    output_file_location = current_working_directory + "/Output"
    commando.touch(output_file_location)
    commando.fls(offset, imagepath, output_file_location)
    print("FLS RETURNED")
    inode_mapping = {}

    file = openFile(output_file_location, "r", verbose)

    # Iterate through the lines using a flexible regular expression to extract the information
    lines = file.readlines()

    for line in lines:
        match = re.search(r'[^:]+ (\d+):[ \t]+(.+)', line)
        if match:
            inode = int(match.group(1))
            filename = match.group(2)
            inode_mapping[filename] = inode

    # Function to get the inode number for a given filename
    def get_inode_number(filename):
        return inode_mapping.get(filename, None)

    # Example usage:
    inode_number = get_inode_number(searched_file)

    if inode_number is not None:
        if verbose:
            print(f"The corresponding inode number for {searched_file} is {inode_number}\n")
        return inode_number
    else:
        print(f"Filename {searched_file} not found in the mapping.")
        writeStderr(f"Filename {searched_file} not found in the mapping.")
        return -1


def extract_all_inodes(imagepath, offset):
    """
    The extract_all_inodes function takes in the path to an image file and the offset of a partition within that image
    file. It then uses fls to extract all of the inodes from that partition, returning them as a list.
    
    :param imagepath: Specify the path to the image file on your computer
    :param offset: Specify the offset of the partition
    :return: A list of all inodes
    
    """
    current_working_directory = os.getcwd()
    output_file_location = current_working_directory + "/Output"
    commando.touch(output_file_location)
    commando.fls(offset, imagepath, output_file_location)

    inode_list = []
    print("Hello1")
    file = openFile(output_file_location, "r", False)
    print("Hello2")

    # Iterate through the lines using a flexible regular expression to extract the information
    lines = file.readlines()
    i = 0
    for line in lines:
        print(i)
        i += 1
        match = re.search(r'[^:]+ (\d+):[ \t]+(.+)', line)
        if match:
            inode = int(match.group(1))
            filename = match.group(2)
            if not filename == "$OrphanFiles":
                inode_list.append(inode)

    return inode_list
