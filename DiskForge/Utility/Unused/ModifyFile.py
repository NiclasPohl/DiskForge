from Utility.SleuthKit.ExtractValuesFromMMLS import mmls_extract_all_partitions, print_partition_list
from Utility.SleuthKit.ExtractValuesFromFLS import extract_values_fls
from Utility.SleuthKit.ExtractValuesFromIstat import istat_extract_inode
from Utility.SleuthKit.ExtractValuesFromFSSTAT import extract_values_fsstat
from Utility.File_Operations.ExtractBytesFromHexFile import extractBytesFromHex
from Utility.FileModification.WriteByteToImageFileData import modify_binary

from subprocess import run, PIPE
#TODO Problem:
'''
Wenn man die Datei Länge mit 0 Bytes Padded ist es ned froh
Okay Problem ist, er will #Dateilänge Bytes einlesen
Die 0 Bytes kann er nicht repräsentieren und dementsprechend ned als Textdatei darstellen
Bedeutet wenn man die Länge Ändern will muss man wahrscheinlich die Inode Metadaten anpassen
0x4 4Byte little Endian Lower 32-bits of size in bytes. 
Sehe aber kein Upper x Bit of Size
Wären nur ca 4,2 Gigabyte?
Kommt mir etwas wenig vor
'''

def modifyFile(image_location=False, file_location=False, partition_num=False, verbose=False):
    # print(image_location, file_location, partition_num, verbose)
    if image_location == None:
        image_location = input("Please enter the image file location: ")
    else:
        image_location = image_location[0]
    if file_location == None:
        file_location = input("Please enter the location of the file which timestamps you want to modify: ")
    file_location = file_location[0]
    if verbose == None:
        verbose = False

    extracted_partitions = mmls_extract_all_partitions(imagepath=image_location, verbose=verbose)
    if partition_num == None:
        print_partition_list(extracted_partitions)
        partition_num = int(input("\nWhat Partition Number do you want to Extract? "))
    else:
        partition_num = partition_num[0]
    partition_to_use = extracted_partitions[partition_num]

    '''
    Step 1: Extract the Inode Number corresponding to the given File Name
    '''
    inode_number = extract_values_fls(imagepath=image_location, offset=str(partition_to_use.start),
                                      searched_file=file_location, verbose=verbose)
    print("Inode Number: " + str(inode_number))

    file_system_metadata = extract_values_fsstat(imagepath=image_location, offset=str(partition_to_use.start),
                                                 verbose=verbose)
    if verbose:
        file_system_metadata.print()

    inode_data = istat_extract_inode(imagepath=image_location, inode_number=inode_number,
                                     offset=str(partition_to_use.start), verbose=verbose)
    command_touch = "touch tempfile"
    run(command_touch, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    command = "icat -o " + str(partition_to_use.start) + " " + str(image_location) + " " + str(inode_number) + " > tempfile"
    run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    input()
    # Als nächstes Hexdump der Datei normalerweise dazwischen erst noch Veränderung
    command_hexdump = "hexdump -C tempfile > newfile"
    run(command_hexdump, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    bytes = extractBytesFromHex("./newfile")
    #print(bytes)
    command_remove = "rm tempfile newfile"
    run(command_remove, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

    modify_binary(blocks=inode_data.blocks,bytes_array=bytes,image_location=image_location,fs_meta=file_system_metadata,sector_size=partition_to_use.sector_size,partition_start=partition_to_use.start)

