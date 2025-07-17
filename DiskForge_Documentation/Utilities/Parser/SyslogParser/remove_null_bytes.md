# remove_null_bytes()
The remove_null_bytes function is used to remove null bytes from a file.
## Parameters:
    def remove_null_bytes(file,verbose=False):
- file: Open the file and read it
- verbose: Print out the number of zero bytes removed
- :return: 0 on success or - 1 on error
## Workflow:
1. Parse File
2. Replace all null bytes