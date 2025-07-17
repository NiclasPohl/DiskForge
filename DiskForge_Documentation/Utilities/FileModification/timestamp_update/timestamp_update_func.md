# timestamp_update()
The function `timestamp_update` modifies timestamps in a file system image based on the specified
    criteria.

## Parameters:
    def timestamp_update(timestamps_to_modify, inode_offset, image_location, timestamps_original, verbose=False, time=None):
-  timestamps_to_modify: `timestamps_to_modify` is a parameter that specifies which timestamps
    to modify. It can be a string indicating a single timestamp type to modify (e.g., "accessed",
    "file_modified", "inode_modified", "file_created", "all"), or a list of strings containing multiple
    timestamp types to modify
-  inode_offset: The `inode_offset` parameter in the `timestamp_update` function is used to
    specify the offset of the inode within the file system. This offset is crucial for locating and
    updating the metadata associated with the specified inode
-  image_location: The `image_location` parameter in the `timestamp_update` function represents
    the location of the image where the timestamps are being modified. This could be a file path or any
    other identifier that specifies the location of the image data
-  timestamps_original: Unused
-  verbose: The `verbose` parameter in the `timestamp_update` function is a boolean flag that
    controls whether additional information or messages should be displayed during the execution of the
    function. When `verbose` is set to `True`, the function may print out more details or status updates
    to the console to provide feedback on, defaults to False (optional)
-  time: The `time` parameter in the `timestamp_update` function is used to specify a specific
    time to update the timestamps to. It can be a single timestamp value or a list of timestamp values
    corresponding to the timestamps to be modified. The function uses this parameter to update the
    specified timestamps in the binary data

## Workflow:
1. Check if `timestamps_to_modify` is `str` or `list`
2. Run the corresponding `modify_binary()` functions