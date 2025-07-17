'''
This is the driver code for all the modules developed inside this framework
Execute this file with the corresponding arguments on the commandline to manipulate the timestamps on ext4
changeTimestamps:
    Lets the user set the timestamps of a given file to arbitrary values
swap_Timestamps:
    Let the user swap the timestamps of two files
copy_Timestamps:
    Let the user copy the timestamp of a source file to a args.target file
nuke_Inode:
    Overwrite the Metadata of a given file with 0-Bytes
scramble:
    Takes the timestamps of two randomly chosen files and swaps them. Does this a number of times specified by counter
shift:
    Shifts the Timestamp by a given value
reset:
    Resets all the timestamps of a given args.target image with the source image
meta:
    Extracts Metadata
mod:
    Modifies File
change_log_ts:
    Change Logfile Timestamp
log_delta:
    Delta Shift on Logfile
firefox_change:
    Change Timestamps in the places.sqlite of firefox
firefox_delta:
    Delta shift for places.sqlite of firefox
'''

import argparse

# Metadata
from Modules.Timestomping.Metadata.Meta_Change import Meta_Change
from Modules.Timestomping.Metadata.FileTimestampSwapper import swap_Timestamps
from Modules.Timestomping.Metadata.CopyTimestamps import copy_Timestamps
from Modules.Timestomping.Metadata.NukeInodes import nuke_Inode
from Modules.Timestomping.Metadata.Scramble_Inodes import scramble
from Modules.Timestomping.Metadata.Meta_DeltaShift import Meta_DeltaShift
from Modules.Timestomping.Metadata.ResetTimestamps import reset_Timestamps

# Browser Database
from Modules.Timestomping.BrowserDatabase.DB_Change import DB_Change
from Modules.Timestomping.BrowserDatabase.DB_DeltaShift import DB_DeltaShift

# Logfiles
from Modules.Timestomping.LogFiles.Log_Change import Log_Change
from Modules.Timestomping.LogFiles.Log_DeltaShift import Log_DeltaShift
from Modules.Timestomping.LogFiles.LogChangeTS_MultiFile import logchangets_multi

# Experimental
from Modules.Experimental.restoreFromLog import find_matching_lines
from Modules.Experimental.File_Extract_And_Writeback_Manual import extractFile, writebackFile

from Utility.Other.WriteTimeModLog import programCompletion, log_execution_time

import time

start = time.time()

parser = argparse.ArgumentParser()

'''
TODO:
    - Help Option pro Argument
    - Evt Default Type bei manchen
'''
parser.add_argument("-v", "--verbosity", action='store_true', help="increase output verbosity")
parser.add_argument("-m", "--mode",
                    choices=["change", "shift", "copy", "swap", "reset", "scramble", "nuke"])
parser.add_argument("--img", type=str, nargs='+', help="path to image file")
parser.add_argument("--file", type=str, nargs='+', help="path to file which you wish to modify")
parser.add_argument("--partnum", type=int, nargs='+', help="Partition Number")
parser.add_argument("--count", type=int,
                    help="Counter for the Scramble Operator, specifies how often the program should scramble")
parser.add_argument("--shift_type", type=str, choices=["second", "minute", "hour", "day"],
                    help="What type of shift e.g. seconds, hours, minutes, days")
parser.add_argument("--shift_time", type=int, help="How much of given type should be shifted")
parser.add_argument("--complex", action='store_true', help="Use complex year generation mechanism")
parser.add_argument("--ts", type=str, nargs="+", help="Target Timestamp YYYY-MM-DD hh-mm-ss")
parser.add_argument("--mess", type=str, nargs="+", help="Target message")
parser.add_argument("--url", type=str, nargs='+', help="Target URL")
parser.add_argument("--nts", type=str, nargs="+", help="New Timestamp YYYY-MM-DD hh-mm-ss")
parser.add_argument("--table", type=str, nargs="+", help="The Table for SQL Queries")
parser.add_argument("--WHERE", type=str, nargs='+',
                    help="The Where Statements. Format <Column1> <Value1> <Column2> <Value2> etc.")
parser.add_argument("--nval", type=str, nargs='+', help="The new Value for DB. Format: <Column> <Value>")
parser.add_argument("--comp_mode", type=str, help="Comparison Mode for SQL Query. Use strict for = else LIKE is used")
parser.add_argument("--log_type", choices=["syslog", "apt", "dpkg", "alternatives"])
parser.add_argument("--target", choices=["metadata", "logfile", "database"])
parser.add_argument("--func", type=str)
parser.add_argument("--db_name", choices=["chrome", "firefox", "chromium", "other"])
parser.add_argument("--prim_key", type=str)
parser.add_argument("--update_length", action='store_true', help="Updates the Length of the value saved in the inode")
parser.add_argument("--timestamp", type=str, nargs='+')

args = parser.parse_args()

# newEntry(args)

'''
Match which args.mode is chosen and run the corresponding programm
Check if all needed data is given
Preset all needed values to False so we can check in the programm what is supplemented
'''

execution_result = 42

match args.func:
    case "timestomp":
        match args.target:
            case "metadata":
                match args.mode:
                    case "change":
                        '''
                        python3 ./DiskForge.py --func timestomp --target metadata --mode change --img /home/niclas/asservat_74382-23.img --file home --partnum 6
                        '''
                        execution_result = Meta_Change(image_location=args.img, file_location=args.file,
                                                       partition_num=args.partnum,
                                                       verbose=args.verbosity, args=args, timestamp=args.timestamp, nts=args.ts)
                    case "shift":
                        '''
                        python3 ./DiskForge.py --func timestomp --target metadata --mode shift --img /home/niclas/asservat_74382-23.img --file home --partnum 6 --shift_type hour --shift_time 13
                        '''
                        execution_result = Meta_DeltaShift(image_location=args.img, file_location=args.file,
                                                           partition_num=args.partnum,
                                                           shift_type=args.shift_type,
                                                           shift_num=args.shift_time, verbose=args.verbosity, args=args, timestamp=args.timestamp)
                    case "copy":
                        execution_result = copy_Timestamps(image_location=args.img, file_location=args.file,
                                                           partition_num=args.partnum,
                                                           verbose=args.verbosity, args=args)
                    case "swap":
                        execution_result = swap_Timestamps(image_location=args.img, file_location=args.file,
                                                           partition_num=args.partnum,
                                                           verbose=args.verbosity, args=args)
                    case "reset":
                        execution_result = reset_Timestamps(image_location=args.img, partition_num=args.partnum,
                                                            verbose=args.verbosity, args=args)
                    # The following Modules are purely experimental. Use with caution.
                    case "scramble":
                        execution_result = scramble(image_location=args.img, partition_num=args.partnum,
                                                    count=args.count,
                                                    verbose=args.verbosity, args=args)
                    case "nuke":
                        execution_result = nuke_Inode(image_location=args.img, file_location=args.file,
                                                      partition_num=args.partnum,
                                                      verbose=args.verbosity, args=args)

            case "logfile":
                match args.mode:
                    case "change":
                        '''
                        python3 ./DiskForge.py --func timestomp --target logfile --mode change --img /home/niclas/Ubuntu.img  --file var/log/syslog --partnum 6 --mess SMBIOS --nts 2024-11-13 20:15:00 --log_type syslog
                        '''
                        execution_result = Log_Change(image_location=args.img, file_location=args.file,
                                                      partition_num=args.partnum,
                                                      complex=args.complex, target_timestamp=args.ts,
                                                      target_message=args.mess,
                                                      new_ts=' '.join(args.nts), verbose=args.verbosity,
                                                      log_type=args.log_type, update=args.update_length, args=args)
                    case "shift":
                        '''
                        python3 ./DiskForge.py --func timestomp --target logfile --mode shift --img /media/niclas/Crucial X6/ManipulatedDiskImages/Logfiles/TemporalForge  --file var/log/syslog --partnum 6 --mess SMBIOS --nts 2024-11-13 20:15:00 --log_type syslog
                        '''
                        execution_result = Log_DeltaShift(image_location=args.img, file_location=args.file,
                                                          partition_num=args.partnum,
                                                          complex=args.complex, target_timestamp=args.ts,
                                                          target_message=args.mess,
                                                          verbose=args.verbosity, shift_type=args.shift_type,
                                                          shift_num=args.shift_time, log_type=args.log_type,
                                                          update=args.update_length, args=args)
                    case "change_multi":
                        execution_result = logchangets_multi(image_location=args.img, file_location=args.file,
                                                             partition_num=args.partnum,
                                                             complex=args.complex, target_timestamp=args.ts,
                                                             target_message=args.mess,
                                                             new_ts=' '.join(args.nts), verbose=args.verbosity,
                                                             log_type=args.log_type, update=args.update_length,
                                                             args=args)

            case "database":
                match args.mode:
                    case "change":
                        '''
                        python3 ./DiskForge.py --func timestomp --target database --mode change --db_name firefox --img /home/niclas/asservat_74382-23.img --file home/kassensystem/snap/firefox/common/.mozilla/firefox/ij9d8zia.default/places.sqlite --partnum 6 --ts 2023-06-09 23:32:32 --url tagesschau --nts 2024-11-12 20:15:00 
                        '''
                        execution_result = DB_Change(image_location=args.img, file_location=args.file,
                                                     partition_num=args.partnum, table=args.table, where=args.WHERE,
                                                     nval=args.nval, comparison_mode=args.comp_mode,
                                                     db_name=args.db_name, target_timestamp=args.ts,
                                                     target_url=args.url, new_ts=args.nts, verbose=args.verbosity,
                                                     primary_key=args.prim_key, update_val=args.update_length,
                                                     args=args)
                    case "shift":
                        '''
                        python3 ./DiskForge.py --func timestomp --target database --mode shift --db_name firefox --img /home/niclas/asservat_74382-23.img --file home/kassensystem/snap/firefox/common/.mozilla/firefox/ij9d8zia.default/places.sqlite --partnum 6 --ts 2023-06-09 23:32:32 --url tagesschau --shift_type hour --shift_time 36                        
                        python3 ./DiskForge.py --func timestomp --target database --mode shift --db_name firefox --img /home/niclas/asservat_74382-23.img --file home/kassensystem/snap/firefox/common/.mozilla/firefox/ij9d8zia.default/places.sqlite --partnum 6 --url tagesschau --shift_type hour --shift_time 36                        
                        '''
                        execution_result = DB_DeltaShift(image_location=args.img, file_location=args.file,
                                                         partition_num=args.partnum, table=args.table, where=args.WHERE,
                                                         nval=args.nval, comparison_mode=args.comp_mode,
                                                         db_name=args.db_name, target_timestamp=args.ts,
                                                         target_url=args.url, new_ts=args.nts, verbose=args.verbosity,
                                                         primary_key=args.prim_key, shift_type=args.shift_type,
                                                         shift_num=args.shift_time, update_val=args.update_length, args=args)

            case "experimental":
                match args.mode:
                    case "redo-log":
                        execution_result = find_matching_lines(args.file)
                    case "extract-file":
                        execution_result = extractFile(image_location=args.img, files=args.file,
                                                       partition_num=args.partnum,
                                                       verbose=args.verbosity, args=args)
                    case "writeback-file":
                        execution_result = writebackFile(image_location=args.img, files=args.file,
                                                         partition_num=args.partnum,
                                                         verbose=args.verbosity, update=args.update_length, args=args)

    case "help":
        execution_result = 0

    case _:
        execution_result = -1

end = time.time()

log_execution_time(end - start)

programCompletion(execution_result)
if execution_result == 42 or execution_result == None:
    print("The Module {} {} {} did not return a value".format(args.func, args.target, args.mode))
if not execution_result == -1:
    print("SUCCESS")
else:
    print("FAILURE")
