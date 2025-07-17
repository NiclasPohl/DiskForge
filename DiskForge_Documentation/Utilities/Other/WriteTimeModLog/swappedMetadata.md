# swappedMetadata()
    The swappedMetadata function takes in a list of data and writes it to the TimeModLogFilePath.
    The data is formatted as follows:
        Inode &lt;inode number&gt; at Offset &lt;offset&gt; with Inode &lt;inode number&gt; at Offset &lt;offset&gt;.\n
## Parameters:
    def swappedMetadata(data):
- data: Pass in the data from the log file
- :return: The inode numbers and offsets of the swapped metadata