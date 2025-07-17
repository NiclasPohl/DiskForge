from Utility.FileModification import Watermark
from Utility.Parser.SyslogParser import remove_null_bytes
from Utility.SleuthKit.ExtractValuesFromFLS import extract_values_fls

from Utility.SleuthKit.ExtractValuesFromMMLS import mmls_extract_all_partitions, print_partition_list

from Utility.FileModification.WriteByteToImageFileData import writeback
import Utility.Other.Terminal_Commands as commando
import os
from Utility.Other.WriteTimeModLog import writeChangedLogEntries, newEntry
from Utility.LogEntryStructures import sys_log
from Utility.LogEntryStructures import dpkg_log, alternatives_log, apt_history

import copy

months_number_to_name = {"1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun", "7": "Jul", "8": "Aug",
                         "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}


def Log_Change(image_location=None, file_location=None, partition_num=None, complex=False,target_timestamp=None, target_message=None, new_ts=None, verbose=False, log_type=None, update=False,args=None):
    """
    This function `Log_Change` is designed to modify timestamps and messages in log files extracted from
    disk images, based on user input and specified criteria.
    
    :param image_location: The `image_location` parameter in the `Log_Change` function is used to
    specify the location of the disk image from which data will be extracted for processing. If this
    parameter is not provided when calling the function, the user will be prompted to enter the image
    file location interactively

    :param file_location: The `file_location` parameter in the `Log_Change` function refers to the
    location of the file whose timestamps you want to modify. If this parameter is not provided when
    calling the function, the user will be prompted to enter the file location via input

    :param partition_num: The `partition_num` parameter in the `Log_Change` function is used to specify
    the partition number from which you want to extract data. It is an integer value that corresponds to
    the partition number on the disk image you are working with. If this parameter is not provided when
    calling the function,

    :param complex: The `complex` parameter in the `Log_Change` function is a boolean flag that
    indicates whether to use a simple or complex mechanism for generating year data when processing log
    files, defaults to False (optional)

    :param target_timestamp: The `target_timestamp` parameter in the `Log_Change` function is used to
    specify the timestamp of the events that you want to target for modification in the log file. It
    allows you to filter and identify specific events based on their timestamp. If you provide a
    `target_timestamp` value, the

    :param target_message: The `target_message` parameter in the `Log_Change` function is used to
    specify a message that you want to target for modification in the log file. This message will be
    used to identify specific log events that you want to change. If the `target_message` parameter is
    provided, it will

    :param new_ts: The `new_ts` parameter in the `Log_Change` function is used to specify the new
    timestamp that you want to assign to the target events in the log file. This parameter allows you to
    update the timestamp of specific events in the log file to a new value that you provide

    :param verbose: The `verbose` parameter in the `Log_Change` function is used to control the level of
    detail in the output messages. When `verbose` is set to `True`, the function will print more
    information and progress updates during its execution. This can be helpful for debugging or
    understanding the process flow, defaults to False (optional)

    :param log_type: The `log_type` parameter in the `Log_Change` function specifies the type of log
    file to be processed. It can take on the following values:

    :param update: The `update` parameter in the `Log_Change` function is a boolean flag that indicates
    whether the function should update the log entries or not. If `update` is set to `True`, the
    function will write the changes back to the disk image. If `update` is set to `, defaults to False
    (optional)
    
    :param args: The `args` parameter in the `Log_Change` function seems to be a dictionary-like object
    that is used to store and pass various arguments throughout the function. It appears to be used to
    keep track of and update values for `image_location`, `file_location`, `partition_num`, and `
    """


    '''
    Checking if all needed parameters are given
    If not ask user via input
    '''
    # Für alle gleich
    if target_timestamp is not None:
        target_timestamp = ' '.join(target_timestamp)
    if target_message is not None:
        target_message = ' '.join(target_message)
    if image_location == None:
        image_location = input("Please enter the image file location: ")
        args.image_location = image_location
    else:
        image_location = "".join(image_location)
    if file_location == None:
        file_location = input("Please enter the location of the file which timestamps you want to modify: ")
        args.file = file_location
    file_location = file_location[0]
    if verbose == None:
        verbose = False

    extracted_partitions = mmls_extract_all_partitions(imagepath=image_location, verbose=verbose)
    if partition_num == None:
        print_partition_list(extracted_partitions)
        partition_num = int(input("\nWhat Partition Number do you want to Extract? "))
        args.partnum = partition_num
    else:
        partition_num = partition_num[0]
    partition_to_use = extracted_partitions[partition_num]
    if new_ts == None:
        new_ts = input("Please enter new timestamp: ")
        args.new_ts = new_ts
    if log_type == None:
        log_type = input("Please enter log_type: ")
        args.log_type = log_type
    newEntry(args)
    log_type = log_type.lower()

    match log_type:
        case "alternatives":
            event_class = alternatives_log
        case "apt":
            event_class = apt_history
        case "dpkg":
            event_class = dpkg_log
        case "auth":
            event_class = sys_log
        case _:
            event_class = sys_log

    compressed_file = False
    last_chars = file_location[-3:]
    if last_chars == ".gz":
        compressed_file = True

    '''
    Extract Inode Number
    '''
    inode_number = extract_values_fls(imagepath=image_location, offset=str(partition_to_use.start),
                                      searched_file=file_location, verbose=verbose)

    if inode_number == -1:
        print("Failure to find file")
        return -1

    '''
    Extract the file from the disk image
    '''
    commando.icat(partition_to_use.start, image_location, inode_number, "./UbuntuSyslog")
    if compressed_file:
        commando.decompress("./UbuntuSyslog")

    '''
    Removing Null Bytes, because these don't belong in the text file
    '''
    remove_null_bytes("./UbuntuSyslog", verbose)

    '''
    Now we parse the LogFile and extract the indivual events
    '''

    # So hier Unterschied
    events = event_class.parseFile("./UbuntuSyslog", verbose)

    if log_type == "syslog":
        if not complex:
            '''
            Simple Year Generation Mechanism
            Uses the file time and looks at the months of the events to detect year skip
            '''
            events = sys_log.year_generator_simple(parsedLogs=events, image_location=image_location,
                                                   inode_number=inode_number, partition_to_use=partition_to_use)

        else:
            '''
            Complex Year Generation Mechanism
            Uses log2timeline to generate year data
            '''
            events = sys_log.year_generator_complex(parsedLogs=events)

    '''
    Identify target events by timestamp and/or message
    '''
    new_events, old_events = event_class.filter_events(events, target_timestamp, target_message)
    new_events_orig = copy.deepcopy(new_events)
    for event in new_events:
        event.change(new_ts)

    writeChangedLogEntries(new_events_orig, new_events)

    events = old_events + new_events
    events.sort()

    event_class.writeback2file("./UbuntuSyslog", events, verbose)

    if compressed_file:
        commando.compress("/UbuntuSyslog")
        logfilepath = os.getcwd() + "/UbuntuSyslog.gz"
    else:
        logfilepath = os.getcwd() + "/UbuntuSyslog"

    if not len(new_events) == 0:
        if (verbose):
            print("Writing changes back to the disk image!")
        writeback(image_location=image_location, partition_to_use=partition_to_use, inode_number=inode_number,
                  file_path=logfilepath, verbose=verbose, update=update)

    Watermark.setWaterMark(partition_to_use.start * int(partition_to_use.sector_size), image_location)

    return 0
