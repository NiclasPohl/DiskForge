# extractBytesFromHex()
The function `extractBytesFromHex` reads a file, extracts hex values excluding the address part,
    converts them to integers, and returns a list of the extracted integers.

## Parameters:
    def extractBytesFromHex(filename, verbose):
-  filename: The function `extractBytesFromHex` seems to be designed to read a file, extract hex
    values excluding the address part, convert them to integers, and return a list of these integers. It
    looks like there are some comments and code snippets that are either incomplete or commented out
-  verbose: The `verbose` parameter in the `extractBytesFromHex` function is used to control
    whether additional information or messages are displayed during the execution of the function. If
    `verbose` is set to `True`, the function may print out progress updates, debug information, or any
    other relevant messages to help
- **return:** The function `extractBytesFromHex` is returning a list of integers that represent the
    extracted hex values from the input file, excluding the address part.

## Workflow:
1. Read all lines from file
2. Write in new file the cuttet lines
3. `hex_values = re.findall(r'\b([0-9a-fA-F]{2})\b', sample_output)`
4. Convert hex to int