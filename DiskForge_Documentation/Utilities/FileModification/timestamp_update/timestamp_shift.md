# timestamp_shift()
The function `timestamp_shift` modifies specified timestamps in a file system image based on the
    provided parameters.
## Parameters:
    def timestamp_shift(timestamps_to_modify, inode_offset, image_location, timestamps_original, second_shift,verbose=False):
-  timestamps_to_modify: timestamps_to_modify is a list of strings indicating which timestamps
    to modify. Possible values include "accessed", "file_modified", "inode_modified", "file_created",
    and "all"
-  inode_offset: The `inode_offset` parameter in the `timestamp_shift` function represents the
    offset value for the inode being modified. It is used to calculate the specific location within the
    image where the timestamps are stored for that particular inode
-  image_location: The `image_location` parameter in the `timestamp_shift` function represents
    the location of the image where the timestamps are being modified. This could be a file path or any
    other identifier that specifies the location of the image data
-  timestamps_original: Unused
-  second_shift: The `second_shift` parameter in the `timestamp_shift` function is used as an offset value for shifting timestamps. It is likely used to adjust the timestamps by a
    certain number of seconds during the shifting process. This parameter allows for flexibility in how
    much the timestamps are shifted by
-  verbose: The `verbose` parameter in the `timestamp_shift` function is a boolean parameter
    that is set to `False` by default. It is used to control whether additional information or details
    should be displayed during the execution of the function. If `verbose` is set to `True`, the
    function may output, defaults to False (optional)

## Workflow:
1. Runs for the given parameters the right `shift_binary` binary method