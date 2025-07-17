# checkifutf8()
The function `checkifutf8` checks if a file is encoded in UTF-8 and returns the result, with an
    option to display the elapsed time for the detection process if verbose mode is enabled.
## Parameters:
    def checkifutf8(filepath, verbose):
-  filepath: The `filepath` parameter is a string that represents the path to the file that you
    want to check for UTF-8 encoding
-  verbose: The `verbose` parameter in the `checkifutf8` function is a boolean flag that
    determines whether additional information or messages should be displayed during the execution of
    the function. If `verbose` is set to `True`, the function will print out the elapsed time for the
    detection of encoding for the file
- **return:** The function `checkifutf8` is returning the result of the `commando.checkIfUTF8(filepath)`
    function call.

## Workflow:
1. Run commando.checkIfUTF8()