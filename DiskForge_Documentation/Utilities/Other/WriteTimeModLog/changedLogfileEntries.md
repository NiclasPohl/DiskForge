# changedLogfileEntries()
The changedLogfileEntries function takes a list of entries as an argument.
    It then opens the TimeModLogFilePath file in append mode and writes to it.
    If the length of the entries list is 0, meaning that there are no changed logfile entries, 
    then it writes &quot;None&quot; to the file. Otherwise, for each entry in the list of changed logfile 
    entries (which is a dictionary), it converts that entry into a string and writes that string 
    to TimeModLogFilePath.

## Parameters:
    def changedLogfileEntries(entries):
- entries: Write the entries to a file
- :return: A list of the logfile entries that have been changed