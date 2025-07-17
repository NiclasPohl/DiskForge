from Utility.FileModification import Watermark
from Utility.Parser.SyslogParser import remove_null_bytes
from Utility.SleuthKit.ExtractValuesFromFLS import extract_values_fls

from Utility.SleuthKit.ExtractValuesFromMMLS import mmls_extract_all_partitions, print_partition_list

from Utility.FileModification.WriteByteToImageFileData import writeback
import Utility.Other.Terminal_Commands as command
import os
from Utility.Other.WriteTimeModLog import writeChangedLogEntries, newEntry
from Utility.LogEntryStructures import sys_log
from Utility.LogEntryStructures import dpkg_log, alternatives_log, apt_history

months_number_to_name = {"1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun", "7": "Jul", "8": "Aug",
                         "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}


def Log_DeltaShift(image_location=None, file_location=None, partition_num=None, complex=None, target_timestamp=None, target_message=None, shift_type=None, shift_num=None, verbose=False, log_type=None, update=False, args=None):

    '''
    Checking if all needed parameters are given
    If not ask user via input
    '''
    # Für alle gleich
    shift_multiplicator = 1

    if target_timestamp is not None:
        target_timestamp = ' '.join(target_timestamp)
    if target_message is not None:
        target_message = ' '.join(target_message)
    else:
        target_message = ""
    if image_location == None:
        image_location = input("Please enter the image file location: ")
        args.image_location = image_location
    else:
        image_location = " ".join(image_location)
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

    if shift_type == None:
        shift_type = input("Please enter what type of shift you want to do (second, minute, hour, day): ")
        args.shift_type = shift_type
    match shift_type:
        case "second":
            shift_multiplicator = 1
        case "minute":
            shift_multiplicator = 60
        case "hour":
            shift_multiplicator = 60 * 60
        case "day":
            shift_multiplicator = 60 * 60 * 24

    if shift_num == None:
        shift_num = int(input("Please enter the number you want to shift by: "))
        args.shift_num = shift_num
    else:
        shift_num = int(shift_num)

    newEntry(args)

    shift_factor_seconds = shift_multiplicator * shift_num

    compressed_file = False
    last_chars = file_location[-3:]
    if (last_chars == ".gz"):
        compressed_file = True

    if log_type == None:
        log_type = input("Please enter log_type: ")
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
    command.icat(partition_to_use.start, image_location, inode_number, "./UbuntuSyslog")

    if compressed_file:
        command.decompress("./UbuntuSyslog")

    '''
    Removing Null Bytes, because these don't belong in the text file
    '''
    remove_null_bytes("./UbuntuSyslog")

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
    new_events_orig = new_events.copy()
    for event in new_events:
        event.shift(shift_factor_seconds)

    writeChangedLogEntries(new_events_orig, new_events)

    events = old_events + new_events
    events.sort()

    event_class.writeback2file("./UbuntuSyslog", events)

    if compressed_file:
        command.compress("/UbuntuSyslog")
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
