# writeTimestampMetaChange()
The writeTimestampMetaChange function takes in two arguments, old and new.
    The function then opens the TimeModLogFilePath file for appending. The function writes to the file:
    &quot;Changed Timestamps:&quot; followed by a newline character, &quot;Accessed from {} to {} \n&quot;.format(old.accessed, new.accessed) 
    followed by a newline character,&quot;Modified from {} to {}\n&quot;.format(old.file_modified, new.file_modified) followed 
    by a newline character,&quot;Changed from {} to {}\n&quot;.format(old.inode_modified,

## Parameters:
    def writeTimestampMetaChange(old, new):
- old: Store the old metadata
- new: New Metadata
- :return: Nothing