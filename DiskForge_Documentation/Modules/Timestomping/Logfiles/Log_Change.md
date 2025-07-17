# Log - Change

The Change module for the Logfiles in the in the file [Log_Change.py](https://faui1-gitlab.cs.fau.de/lena.voigt/diskforge/-/blob/main/DiskForge/Modules/Timestomping/LogFiles/Log_Change.py).

It contains the function *Log_Change* which uses the following parameters:

    def Log_Change(image_location=None, file_location=None, partition_num=None, complex=False,target_timestamp=None, target_message=None, new_ts=None, verbose=False, log_type=None, update=False,args=None):

 - image_location: The `image_location` parameter in the `Log_Change` function is used to specify the location of the disk image from which data will be extracted for processing.
 - file_location: The `file_location` parameter in the `Log_Change` function refers to the
    location of the file whose timestamps you want to modify. If this parameter is not provided when
    calling the function, the user will be prompted to enter the file location via input

 - partition_num: The `partition_num` parameter in the `Log_Change` function is used to specify
    the partition number from which you want to extract data. It is an integer value that corresponds to
    the partition number on the disk image you are working with. If this parameter is not provided when
    calling the function,

 - complex: The `complex` parameter in the `Log_Change` function is a boolean flag that
    indicates whether to use a simple or complex mechanism for generating year data when processing log
    files, defaults to False (optional)

 - target_timestamp: The `target_timestamp` parameter in the `Log_Change` function is used to
    specify the timestamp of the events that you want to target for modification in the log file. It
    allows you to filter and identify specific events based on their timestamp. If you provide a
    `target_timestamp` value, the

 - target_message: The `target_message` parameter in the `Log_Change` function is used to
    specify a message that you want to target for modification in the log file. This message will be
    used to identify specific log events that you want to change. If the `target_message` parameter is
    provided, it will

 - new_ts: The `new_ts` parameter in the `Log_Change` function is used to specify the new
    timestamp that you want to assign to the target events in the log file. This parameter allows you to
    update the timestamp of specific events in the log file to a new value that you provide

 - verbose: The `verbose` parameter in the `Log_Change` function is used to control the level of
    detail in the output messages. When `verbose` is set to `True`, the function will print more
    information and progress updates during its execution. This can be helpful for debugging or
    understanding the process flow, defaults to False (optional)

 - log_type: The `log_type` parameter in the `Log_Change` function specifies the type of log
    file to be processed. It can take on the following values:

 - update: The `update` parameter in the `Log_Change` function is a boolean flag that indicates
    whether the function should update the log entries or not. If `update` is set to `True`, the
    function will write the changes back to the disk image. If `update` is set to `, defaults to False
    (optional)

Workflow:
1. Extract Inode Number Corresponding to Filename
2. Extract File
3. Remove Null Bytes
4. Extract Events
5. If needed: Generate Year
6. Change Timestamp of filtered events
7. Sort all events
8. Write events back to file
9. Write file to disk image