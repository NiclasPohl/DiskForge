# changedDBEntries()
The changedDBEntries function takes in a list of entries that have been changed and writes them to the TimeModLogFilePath.
    It also adds a header explaining what the following entries are.
## Parameters:
    def changedDBEntries(entries):
- entries: Write the entries that were changed in the database to a file
- :return: A list of entries that have been changed