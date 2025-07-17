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


def logchangets_multi(image_location=None, file_location=None, partition_num=None, complex=False,
                      target_timestamp=None, target_message=None, new_ts=None, verbose=False, log_type=None,
                      update=False,
                      args=None):
    '''
    Method for Changing the Timestamp of a logfile
    :param log_type: Type of Log we want to manipulate
    :param image_location: The Path of the image file on the users computer
    :param file_location: The Path of the file inside the image file
    :param partition_num: The Partition Number of the file inside the image file
    :param complex: Use complex mode for generating the missing year data (use log2timeline)
    :param target_timestamp: The Timestamp on which you want to match
    :param target_message: The message on which you want to match
    :param new_ts: The new timestamp you want to set
    :param verbose: Activate for more output
    :return: 0 on success or -1 on error
    '''

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
        image_location = image_location[0]
    if file_location == None:
        file_location = input("Please enter the location of the file which timestamps you want to modify: ")
        file_location = file_location.split(" ")
        args.file = file_location
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

    compressed_file = []
    for file in file_location:
        last_chars = file[-3:]
        if last_chars == ".gz":
            compressed_file.append(True)
        else:
            compressed_file.append(False)

    '''
    Extract Inode Number
    '''
    inode_number = []
    for file in file_location:
        inode_number.append(extract_values_fls(imagepath=image_location, offset=str(partition_to_use.start),
                                               searched_file=file, verbose=verbose))

    for number in inode_number:
        if number == -1:
            print("Failure to find file")
            return -1

    '''
    Extract the file from the disk image
    '''
    events = []
    eventslength = []
    for i in range(len(file_location)):
        filename = f"./file{i}"
        commando.icat(partition_to_use.start, image_location, inode_number, filename)
        if compressed_file[i]:
            commando.decompress(filename)
        remove_null_bytes(filename, verbose)
        events_part = event_class.parseFile(filename)
        if event_class == sys_log:
            if not complex:
                '''
                Simple Year Generation Mechanism
                Uses the file time and looks at the months of the events to detect year skip
                '''
                events_part = sys_log.year_generator_simple(parsedLogs=events_part, image_location=image_location,
                                                            inode_number=inode_number[i],
                                                            partition_to_use=partition_to_use)

            else:
                '''
                Complex Year Generation Mechanism
                Uses log2timeline to generate year data
                '''
                events_part = sys_log.year_generator_complex(parsedLogs=events_part)
        eventslength.append(len(events_part))
        events = events + events_part

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

    counter = 0
    for i in range(len(file_location)):
        temp_events = []
        for j in range(eventslength[i]):
            temp_events.append(events[counter])
            counter += 1
        filename = f"./file{i}"
        event_class.writeback2file(filename, temp_events)
        if compressed_file[i]:
            commando.compress(filename)
            filename += ".gz"
        logfilepath = os.getcwd() + filename
        if (verbose):
            print(f"Now writing back file{i}")
        writeback(image_location=image_location, partition_to_use=partition_to_use, inode_number=inode_number[i],
                  file_path=logfilepath, verbose=verbose, update=update)

    return 0
