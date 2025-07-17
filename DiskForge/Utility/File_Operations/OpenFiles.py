# import chardet
import time

import chardet

from Utility.Other.WriteTimeModLog import writeStderr
import Utility.Other.Terminal_Commands as commando

'''
This Code is just for one problem
Sometimes files are UTF8 encoded and sometimes Latin1
If we now have an ä,ö,ü stuff brakes
This is to mitigate this problem
'''


def detect_encoding_deprecated(file_path, verbose):
    """
    The function `detect_encoding_deprecated` reads a file and detects its encoding using the `chardet`
    library, with an option to display the elapsed time if specified.
    
    :param file_path: The `file_path` parameter is a string that represents the path to the file for
    which you want to detect the encoding. This function reads the contents of the file in binary mode
    and uses the `chardet` library to detect the encoding of the file. If the `verbose` parameter is
    :param verbose: The `verbose` parameter in the `detect_encoding_deprecated` function is a boolean
    flag that determines whether additional information will be printed during the execution of the
    function. If `verbose` is set to `True`, the function will print out the elapsed time for detecting
    the encoding of the file specified by
    :return: The function `detect_encoding_deprecated` returns the encoding detected by the `chardet`
    library for the file located at the specified `file_path`.
    """
    start = time.time()
    with open(file_path, 'rb') as rawfile:
        result = chardet.detect(rawfile.read())
        rawfile.close()
    end = time.time()
    if verbose:
        print("Elapsed Time for {}: {}".format(file_path, end - start))
    return result['encoding']


def detect_encoding_faster_deprecated(filepath, verbose):
    start = time.time()
    res = commando.getFileEncoding(filepath)
    end = time.time()
    if verbose:
        print("Elapsed Time for {}: {}".format(filepath, end - start))
    return res


def checkifutf8(filepath, verbose):
    """
    The function `checkifutf8` checks if a file is encoded in UTF-8 and returns the result, with an
    option to display the elapsed time for the detection process if verbose mode is enabled.
    
    :param filepath: The `filepath` parameter is a string that represents the path to the file that you
    want to check for UTF-8 encoding
    :param verbose: The `verbose` parameter in the `checkifutf8` function is a boolean flag that
    determines whether additional information or messages should be displayed during the execution of
    the function. If `verbose` is set to `True`, the function will print out the elapsed time for the
    detection of encoding for the
    :return: The function `checkifutf8` is returning the result of the `commando.checkIfUTF8(filepath)`
    function call.
    """
    #start = time.time()
    res = commando.checkIfUTF8(filepath)
    #end = time.time()
    if verbose:
        print("Elapsed Time for detection of encoding for {}: {}".format(filepath, end - start))
    return res


def openFile(filepath, mode, verbose):
    """
    The function `openFile` opens a file with a specified mode and detects the encoding of the file,
    handling exceptions and providing verbose output if specified.
    
    :param filepath: The `filepath` parameter is a string that represents the path to the file that you
    want to open or interact with in your Python code. It should include the full path to the file,
    including the file name and extension
    :param mode: The `mode` parameter in the `openFile` function specifies the mode in which the file
    should be opened. It determines whether the file should be opened for reading, writing, or both, and
    whether the file should be created if it does not exist.
    :param verbose: The `verbose` parameter in the `openFile` function is a boolean flag that determines
    whether additional information should be printed during the file opening process. If `verbose` is
    `True`, the function will print out details such as the detected encoding for the file being opened.
    :return: The function `openFile` will return either the opened file object if successful, or -1 if
    an OSError occurs during the file opening process.
    """
    # detected_encoding = detect_encoding(filepath)
    # detected_encoding = detect_encoding_faster(filepath)
    detected_encoding = checkifutf8(filepath, verbose)
    if verbose:
        print(f"For file {filepath} the detected encoding is {detected_encoding}\n")
        # print(detected_encoding)
    try:
        file = open(filepath, mode, encoding=detected_encoding)
        return file

    except OSError as e:
        writeStderr(f"{type(e)}: {e}")
        print(f"{type(e)}: {e}")
        return -1
