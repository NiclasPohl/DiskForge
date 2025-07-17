# extract_bytes_from_hex_without_zero()
This Python function aims to extract non-zero byte values from a hexadecimal dump file.
## Parameters:
    def extract_bytes_from_hex_without_zero(filename, verbose):
-  filename: The function `extract_bytes_from_hex_without_zero` seems to be designed to read a
    file, extract hex values excluding the address part, and return a list of integer values
    corresponding to those hex values that are not equal to 0
-  verbose: The `verbose` parameter in the `extract_bytes_from_hex_without_zero` function is
    used to control whether additional information or messages are displayed during the execution of the
    function. If `verbose` is set to `True`, the function may print out more details or messages to
    provide insights into the processing steps
- **return:** The function `extract_bytes_from_hex_without_zero` is returning a list of integer values
    extracted from a hexadecimal representation in the specified file, excluding any occurrences of the
    value 0.

## Workflow:
1. Parse File
2. Filter out all zeros