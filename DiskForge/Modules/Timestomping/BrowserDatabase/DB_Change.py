from Utility.FileModification import Watermark
from Utility.Other.WriteTimeModLog import writeStderr, writeChangedDBEntries, newEntry
from Utility.DatabaseStructures import chrome_history, database, firefox_places

from Utility.SleuthKit.ExtractValuesFromFLS import extract_values_fls

from Utility.SleuthKit.ExtractValuesFromMMLS import mmls_extract_all_partitions, print_partition_list
from Utility.FileModification.WriteByteToImageFileData import writeback
from Utility.Conversions.Time2EpochMicro import timestamp_to_epoch_micro_bounds
import Utility.Other.Terminal_Commands as command
import os


def DB_Change(image_location=None, file_location=None, partition_num=None, table=None, where=None, nval=None,
              comparison_mode=None, db_name=None, target_timestamp=None, target_url=None, new_ts=None,
              verbose=False, primary_key=None, update_val=False, args=None):
    """
    Change the Timestamp of events in the places.sqlite of firefox
    :param image_location: The Path of the image file on the users computer
    :param file_location: The Path of the file inside the image file
    :param partition_num: The Partition Number of the file inside the image file
    :param target_timestamp: The Timestamp on which you want to match
    :param target_url: The target URL on which you want to match
    :param new_ts: The new timestamp you want to set
    :param verbose: Activate for more output
    :return: Returns -1 on Error
    """

    '''
    Check if all needed values are given
    If not ask user for missing data
    '''
    if image_location == None:
        image_location = input("Please enter the image file location: ")
        args.image_location = image_location
    else:
        image_location = " ".join(image_location)
    if file_location == None:
        file_location = input("Please enter the location of the file which timestamps you want to modify: ")
        args.file_location = file_location
    else:
        file_location = " ".join(file_location)
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

    if target_timestamp is not None:
        target_timestamp = ' '.join(target_timestamp)
        target_timestamp += " UTC"
        target_timestamp = timestamp_to_epoch_micro_bounds(target_timestamp)
    if target_url is not None:
        target_url = ' '.join(target_url)

    if new_ts == None:
        new_ts = input("Please enter new timestamp")
        args.new_ts = new_ts
    else:
        new_ts = ' '.join(new_ts)

    new_ts += " UTC"

    new_ts = timestamp_to_epoch_micro_bounds(new_ts)[0]

    compressed_file = False
    last_chars = file_location[-3:]
    if (last_chars == ".gz"):
        compressed_file = True

    match db_name:
        case "firefox":
            db_interface = firefox_places
            table = "moz_places"
            changed_column = "last_visit_date"
            primary_key = "id"
        case "chrome":
            db_interface = chrome_history
            table = "urls"
            changed_column = "last_visit_time"
            primary_key = "id"
        case "chromium":
            db_interface = chrome_history
            table = "urls"
            changed_column = "last_visit_time"
            primary_key = "id"
        case _:
            db_interface = database
            if nval is None:
                nval = input("Pleaser enter the nval: ")
                args.nval = nval
            changed_column = nval[0]
            if primary_key is None:
                primary_key = "id"
            if table is None:
                table = input("Please enter the table: ")
                args.table = table

    newEntry(args)

    '''
    Extract the Inode Number corresponding to the given File Name
    '''
    inode_number = extract_values_fls(imagepath=image_location, offset=str(partition_to_use.start),
                                      searched_file=file_location, verbose=verbose)
    if (inode_number == -1):
        print("Failure to find file")
        writeStderr("Failure to find file")
        return -1

    '''
    Extract the DB file
    '''
    '''
    We want to copy here because it should be faster than icat twice
    '''
    command.icat(partition_to_use.start, image_location, inode_number, "./places.sqlite")
    if (compressed_file):
        command.decompress("./places.sqlite")

    result_copy = command.copy("./places.sqlite", "./places_orig.sqlite")

    query, update = db_interface.change(target_timestamp=target_timestamp, target_url=target_url, new_ts=new_ts,
                                        table=table, nval=nval,
                                        where=where, comparison_mode=comparison_mode)

    if verbose:
        print("The two following SQL Queries are used:")
        print("Query: {}".format(query))
        print("Update: {}".format(update))

    columns = database.getColumns("places.sqlite", table)

    entries_old = database.update_database(filename="./places.sqlite", query=query, update=update)
    if verbose:
        print(f"{len(entries_old)} entries were modified:")
        print("These are the entries before they were modified:")
        print(entries_old)
        print()
    if not result_copy == -1:
        entries_new = database.compare2databases(file_new="./places.sqlite", file_old="./places_orig.sqlite",
                                                 table=table,
                                                 changed_value_column=changed_column, primary_key=primary_key)
        if verbose:
            print("These are the entries after they were modified:")
            print(entries_new)
            print()
        writeChangedDBEntries(entries_old, entries_new, columns)
    else:
        writeChangedDBEntries(entries_old, ["Error"], columns)

    if (compressed_file):
        command.compress("/places.sqlite")
        places_sqlite = os.getcwd() + "/places.sqlite.gz"
    else:
        places_sqlite = os.getcwd() + "/places.sqlite"
    if not len(entries_old) == 0:
        if (verbose):
            print("Writing back the changes to the disk image!")
        writeback(image_location=image_location, partition_to_use=partition_to_use, inode_number=inode_number,
                  file_path=places_sqlite, verbose=verbose, update=update_val)
    Watermark.setWaterMark(partition_to_use.start * int(partition_to_use.sector_size), image_location)
    return 0
