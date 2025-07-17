from Utility.SleuthKit.ExtractValuesFromFLS import extract_values_fls
from Utility.SleuthKit.ExtractValuesFromMMLS import mmls_extract_specific_partition


def findTimestamps():
    imageFile = input('Enter Location and Name of your Imagefile: ')
    analyseFile = input('Enter Location and Name of File you want to Analyse: ')
    partition = mmls_extract_specific_partition(imagepath=imageFile)
    partition_offset = partition.start
    inode_num = extract_values_fls(searched_file=analyseFile, imagepath=imageFile, offset=partition_offset)
