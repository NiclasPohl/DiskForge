import re

from Utility.File_Operations.OpenFiles import openFile


def extractBytesFromHex(filename, verbose):
    """
    The function `extractBytesFromHex` reads a file, extracts hex values excluding the address part,
    converts them to integers, and returns a list of the extracted integers.
    
    :param filename: The function `extractBytesFromHex` seems to be designed to read a file, extract hex
    values excluding the address part, convert them to integers, and return a list of these integers. It
    looks like there are some comments and code snippets that are either incomplete or commented out
    :param verbose: The `verbose` parameter in the `extractBytesFromHex` function is used to control
    whether additional information or messages are displayed during the execution of the function. If
    `verbose` is set to `True`, the function may print out progress updates, debug information, or any
    other relevant messages to help
    :return: The function `extractBytesFromHex` is returning a list of integers that represent the
    extracted hex values from the input file, excluding the address part.
    """
    # Specify the path to your file
    file_path = filename
    '''
    Für Zukunfts Niclas:
    Der Output von Hexdump sieht so aus:
    00000000  4e 6f 76 20 32 33 20 31  35 3a 32 34 3a 34 36 20  |Nov 23 15:24:46 |
    Dein Algorithmus sucht nach Vorkommen von 0-9 und a-f
    Dein Datum rechts kann auch als Hexbytes interpretiert werden
    Deshalb hattest du danach in der nächsten Zeile das
    00000010  23 15 24 46 6e 69 63 6c  61 73 2d 56 69 72 74 75  |#.$Fniclas-Virtu|
    Die ersten 4 Stück sind das Datum die gehören da gar ned rein
    Deshalb cutten wir nun einfach für jede Zeile vorne und hinten den ramsch den wir ned brauchen weg!
    '''
    # Read the sample text from the file
    file = openFile(file_path, "r", verbose=verbose)
    lines = file.readlines()
    sample_output = file.read()
    file.close()

    file = openFile(file_path, "w", verbose=verbose)
    for line in lines:
        line = line[9:59]
        file.write(line)
    file.close()

    file = openFile(file_path, "r", verbose)
    sample_output = file.read()
    file.close()
    # print(sample_output)

    # Extract hex values excluding the address part
    hex_values = re.findall(r'\b([0-9a-fA-F]{2})\b', sample_output)

    # Print the extracted hex values
    # allBytes = []
    # allHex = []
    allInt = []
    for i in hex_values:
        # allHex.append(i)
        # allBytes.append(bytes.fromhex(i))
        allInt.append(int(i, 16))
    # file = open("allHex.txt", "w")
    # counter = 0
    '''for item in allHex:
        file.write(item + " ")
        if counter % 8 == 0:
            file.write("\n")
        counter += 1'''
    return allInt


def extract_bytes_from_hex_without_zero(filename, verbose):
    """
    This Python function aims to extract non-zero byte values from a hexadecimal dump file.
    
    :param filename: The function `extract_bytes_from_hex_without_zero` seems to be designed to read a
    file, extract hex values excluding the address part, and return a list of integer values
    corresponding to those hex values that are not equal to 0
    :param verbose: The `verbose` parameter in the `extract_bytes_from_hex_without_zero` function is
    used to control whether additional information or messages are displayed during the execution of the
    function. If `verbose` is set to `True`, the function may print out more details or messages to
    provide insights into the processing steps
    :return: The function `extract_bytes_from_hex_without_zero` is returning a list of integer values
    extracted from a hexadecimal representation in the specified file, excluding any occurrences of the
    value 0.
    """
    # Specify the path to your file
    file_path = filename
    '''
    Für Zukunfts Niclas:
    Der Output von Hexdump sieht so aus:
    00000000  4e 6f 76 20 32 33 20 31  35 3a 32 34 3a 34 36 20  |Nov 23 15:24:46 |
    Dein Algorithmus sucht nach Vorkommen von 0-9 und a-f
    Dein Datum rechts kann auch als Hexbytes interpretiert werden
    Deshalb hattest du danach in der nächsten Zeile das
    00000010  23 15 24 46 6e 69 63 6c  61 73 2d 56 69 72 74 75  |#.$Fniclas-Virtu|
    Die ersten 4 Stück sind das Datum die gehören da gar ned rein
    Deshalb cutten wir nun einfach für jede Zeile vorne und hinten den ramsch den wir ned brauchen weg!
    
    Problem: Hexdump lässt lange 0er folgen weg!!!
    Solved: Hexdump -v
    '''
    # TODO

    # Read the sample text from the file
    file = openFile(file_path, "r", verbose=verbose)
    lines = file.readlines()
    sample_output = file.read()
    file.close()

    file = openFile(file_path, "w", verbose=verbose)
    newlines = []
    for line in lines:
        line = line[9:59]
        newlines.append(line)
        file.write(line)
    file.close()

    file = openFile(file_path, "r", verbose=verbose)
    sample_output = file.read()
    file.close()

    # Extract hex values excluding the address part
    hex_values = re.findall(r'\b([0-9a-fA-F]{2})\b', sample_output)

    # Print the extracted hex values

    allInt = []
    for i in hex_values:

        x = int(i, 16)
        if not x == 0:
            allInt.append(int(i, 16))

    '''for item in allHex:
        file.write(item + " ")
        if counter % 8 == 0:
            file.write("\n")
        counter += 1'''
    return allInt

