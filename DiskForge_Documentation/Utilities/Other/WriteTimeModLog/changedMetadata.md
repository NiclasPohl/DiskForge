# changedMetadata()
The changedMetadata function takes in a list of data and writes it to the TimeModLogFilePath.
    The first element of the list is a string containing all elements from the original metadata,
    and the second element is an integer representing where in memory that metadata was found.
## Parameters:
    def changedMetadata(data):
- data: Store the data that is being written to the file
- :return: A list of the changed metadata