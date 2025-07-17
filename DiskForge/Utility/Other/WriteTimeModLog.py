from datetime import datetime

TimeModLogFilePath = "./DiskForge_Logfile"

import csv
from tabulate import tabulate


def newEntry(args):
    """
    The newEntry function is used to log the time and arguments of a function call.
    It takes one argument, args, which should be a list of strings containing the names
    of all arguments passed to the function being logged. It then writes this information
    to TimeModLogFilePath.
    
    :param args: Write the arguments passed to the function
    :return: Nothing
    
    """
    with open(TimeModLogFilePath, 'a') as f:
        f.write("\n\n" + str(datetime.now()) + "\n")
        f.write(str(args) + "\n")


def changedDBEntries(entries):
    """
    The changedDBEntries function takes in a list of entries that have been changed and writes them to the TimeModLogFilePath.
    It also adds a header explaining what the following entries are.
    
    :param entries: Write the entries that were changed in the database to a file
    :return: A list of entries that have been changed
    
    """
    with open(TimeModLogFilePath, 'a') as f:
        f.write("Changed DB Entries: \n")
        if len(entries) == 0:
            f.write("None\n")
        for entry in entries:
            f.write(str(entry) + "\n")


def changedLogfileEntries(entries):
    """
    The changedLogfileEntries function takes a list of entries as an argument.
    It then opens the TimeModLogFilePath file in append mode and writes to it.
    If the length of the entries list is 0, meaning that there are no changed logfile entries, 
    then it writes &quot;None&quot; to the file. Otherwise, for each entry in the list of changed logfile 
    entries (which is a dictionary), it converts that entry into a string and writes that string 
    to TimeModLogFilePath.
    
    :param entries: Write the entries to a file
    :return: A list of the logfile entries that have been changed
    
    """
    with open(TimeModLogFilePath, 'a') as f:
        f.write("Changed Logfile Entries: \n")
        if len(entries) == 0:
            f.write("None")
        for entry in entries:
            f.write(str(entry))


def changedMetadata(data):
    """
    The changedMetadata function takes in a list of data and writes it to the TimeModLogFilePath.
    The first element of the list is a string containing all elements from the original metadata,
    and the second element is an integer representing where in memory that metadata was found.
    
    :param data: Store the data that is being written to the file
    :return: A list of the changed metadata
    
    """
    with open(TimeModLogFilePath, 'a') as f:
        f.write("Changed Metadata:\n")
        f.write(" ".join(data[0]) + " @ Offset: {}\n".format(data[1]))


def swappedMetadata(data):
    """
    The swappedMetadata function takes in a list of data and writes it to the TimeModLogFilePath.
    The data is formatted as follows:
        Inode &lt;inode number&gt; at Offset &lt;offset&gt; with Inode &lt;inode number&gt; at Offset &lt;offset&gt;.\n
    
    :param data: Pass in the data from the log file
    :return: The inode numbers and offsets of the swapped metadata
    
    """
    with open(TimeModLogFilePath, 'a') as f:
        f.write("Swapped Metadata:\n")
        f.write("Inode {} at Offset {} with Inode {} at Offset {}".format(data[0], data[1], data[2], data[3]))


def writeStderr(data):
    """
    The writeStderr function takes a string as an argument and writes it to the TimeModLogFilePath file.
    It is used for logging errors that occur during execution of the program.
    
    :param data: Write the data to the log file
    :return: -1 if the data is empty
    
    """
    if not data == "":
        with open(TimeModLogFilePath, 'a') as f:
            f.write("Error:\n")
            f.write(data)
        return -1
    return 0


def writeTimestampMetaChange(old, new):
    """
    The writeTimestampMetaChange function takes in two arguments, old and new.
    The function then opens the TimeModLogFilePath file for appending. The function writes to the file:
    &quot;Changed Timestamps:&quot; followed by a newline character, &quot;Accessed from {} to {} \n&quot;.format(old.accessed, new.accessed) 
    followed by a newline character,&quot;Modified from {} to {}\n&quot;.format(old.file_modified, new.file_modified) followed 
    by a newline character,&quot;Changed from {} to {}\n&quot;.format(old.inode_modified,
    
    :param old: Store the old metadata
    :param new: Determine whether the file is new or not
    :return: A string
    
    """
    with open(TimeModLogFilePath, 'a') as f:
        f.write("Changed Timestamps:\n")
        f.write("Accessed from {} to {} \n".format(old.accessed, new.accessed))
        f.write("Modified from {} to {}\n".format(old.file_modified, new.file_modified))
        f.write("Changed from {} to {}\n".format(old.inode_modified, new.inode_modified))
        f.write("Created from {} to {}\n".format(old.file_created, new.file_created))


def writeChangedDBEntries_Deprecated(old, new, columns):
    """
    The writeChangedDBEntries_Deprecated function writes the changed entries in a database file to the log file.
    
    :param old: Store the old data from the database
    :param new: Write the new time to the log file
    :param columns: Determine which columns to print out in the log file
    :return: A string that is written to the log file
    
    """
    with open(TimeModLogFilePath, 'a') as f:
        f.write("Changed DB File Entries: \n")
        if len(old) == 0:
            f.write("None Changed. No matching entries found.\n")
        else:
            f.write("{}\n".format(columns))
            columns = columns.split(" |")
            for i in range(len(old)):
                f.write("Old: {}\n".format(old[i]))
                if i < len(new):
                    f.write("New: {}\n".format(new[i]))


def writeChangedDBEntries(old, new, columns):
    """
    Function to write the Changed Database entries
    
    :param old: Old Entries
    :param new: New Entries
    :param columns: Format the table
    :return: Nothing
    
    """
    with open(TimeModLogFilePath, 'a') as f:
        f.write("Changed {} DB File Entries: \n".format(len(old)))
        if len(old) == 0:
            f.write("None Changed. No matching entries found.\n")
    if not len(old) == 0:
        columns = columns.replace(" ", "")
        columns = columns.split("|")
        columns = [""] + columns
        data = [columns]
        # f.write("{}\n".format(columns))
        for i in range(len(old)):
            oldi = list(old[i])
            oldi = ["Old:"] + oldi
            data.append(oldi)
            # f.write("Old: {}\n".format(old[i]))
            if i < len(new):
                newi = list(new[i])
                newi = ["New:"] + newi
                data.append(newi)
                data.append([])
        with open('temp.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerows(data)

        with open('temp.csv', 'r') as csv_file:
            table = tabulate(csv.reader(csv_file), headers="firstrow", tablefmt="plain")

        # Writing the formatted table to a text file
        with open(TimeModLogFilePath, 'a') as txt_file:
            txt_file.write(table)


def writeChangedLogEntries(old, new):
    """
    The writeChangedLogEntries function writes the changed log entries to a file.
    
    :param old: Write the old log entries that were changed
    :param new: Write the new log entries to the file
    :return: Nothing
    
    """
    with open(TimeModLogFilePath, 'a') as f:
        f.write("Changed {} Log File Entries: \n".format(len(old)))
        if len(old) == 0:
            f.write("None Changed. No matching entries found.\n")

        for i in range(len(old)):
            f.write("Old: {}\n".format(old[i].writeback()))
            if i < len(new):
                f.write("New: {}\n".format(new[i].writeback()))
            f.write("\n")


def programCompletion(number):
    """
    The programCompletion function is used to log the success or failure of a program.
        It takes one argument, which is an integer. If the number passed in is - 1, then it logs that there was a failure.
        Otherwise, it logs that there was a success.
    
    :param number: Determine whether the program was successful or not
    :return: Nothing
    
    """
    with open(TimeModLogFilePath, 'a') as f:
        if (number == -1):
            f.write("Failure!\n")
        else:
            f.write("Success!\n")


def log_execution_time(time):
    """
    The log_execution_time function takes in a time parameter and writes it to the TimeModLogFilePath file.
        The function is used to log the execution time of other functions.
    
    :param time: Write the execution time to a file
    :return: Nothing
    
    """
    with open(TimeModLogFilePath, 'a') as f:
        f.write("The execution time was {} seconds!\n".format(time))


def file_to_large(byte_number):
    """
    The file_to_large function is used to write an error message to the TimeModLogFilePath file.
    The function takes one argument, byte_number, which is the number of bytes that couldn't be written.
    
    :param byte_number: Tell the user how many bytes couldn't be written
    :return: Nothing
    
    """
    with open(TimeModLogFilePath, 'a') as f:
        print("Error the file you wanted to write was to large")
        print("{} Bytes couldn't be written".format(byte_number))
