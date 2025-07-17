# openFile()
The function `openFile` opens a file with a specified mode and detects the encoding of the file,
    handling exceptions and providing verbose output if specified.

## Parameters:
    def openFile(filepath, mode, verbose):
-  filepath: The `filepath` parameter is a string that represents the path to the file that you
    want to open or interact with in your Python code. It should include the full path to the file,
    including the file name and extension
-  mode: The `mode` parameter in the `openFile` function specifies the mode in which the file
    should be opened. It determines whether the file should be opened for reading, writing, or both, and
    whether the file should be created if it does not exist.
-  verbose: The `verbose` parameter in the `openFile` function is a boolean flag that determines
    whether additional information should be printed during the file opening process. If `verbose` is
    `True`, the function will print out details such as the detected encoding for the file being opened.
- **return:** The function `openFile` will return either the opened file object if successful, or -1 if
    an OSError occurs during the file opening process.

## Workflow:
1. Detect Encoding using checkifutf8
2. Try opening file with detected encoding