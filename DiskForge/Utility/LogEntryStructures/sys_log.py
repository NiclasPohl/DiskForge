from Utility.Other import ParseTimestamps
from Utility.Parser import CSVParser
from Utility.Parser.SyslogParser import generate_epochtime
from Utility.SleuthKit.ExtractValuesFromIstat import istat_extract_inode
from Utility.Conversions.Timestamp_to_unixtime import date_and_time_2_unixtime, unixtime2apttime
from Utility.Other.WriteTimeModLog import writeStderr
import Utility.Other.Terminal_Commands as commando
from Utility.File_Operations.OpenFiles import openFile

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
months2 = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
           "Nov": 11, "Dec": 12}


class syslog_event:
    timestamp = ""
    year = ""
    timestamp_unix = ""
    message = ""
    audit = False

    def __init__(self, line):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the object with all of its attributes and methods.
        
        
        :param self: Represent the instance of the class
        :param line: Split the line into a list of strings
        :return: Nothing
        
        """
        line = line.split(" ")
        self.timestamp = "{} {} {}".format(line[0], line[1], line[2])
        self.message = ' '.join(line[3::])
        self.message.replace("\n","")
        if self.message.__contains__("audit("):
            self.audit = True

    def __lt__(self, other):
        """
        The __lt__ function is used to compare two objects.
        The function returns True if the object on the left side of the comparison operator is less than (i.e., comes before)
        the object on the right side of the comparison operator, and False otherwise.
        
        :param self: Refer to the current instance of a class
        :param other: Compare the timestamp_unix of two objects
        :return: A boolean value
        
        """
        return self.timestamp_unix < other.timestamp_unix

    def change(self, new_ts):
        """
        The change function takes a new timestamp and changes the current timestamp to that one.
        It also updates the unix time stamp, as well as the message.
        
        :param self: Represent the instance of the class
        :param new_ts: Change the timestamp of a message
        :return: The new timestamp
        
        """
        date, time = new_ts.split()
        print(date)
        old_unix_time = str(self.timestamp_unix)
        self.timestamp_unix = date_and_time_2_unixtime(date, time)
        print(date)
        year, month, day = date.split("-")
        print(f"{month} {day} {time}")
        month = months[int(month) - 1]
        print(f"{month} {day} {time}")
        self.timestamp = "{} {} {}".format(month, day, time)
        print(self.timestamp)
        self.message.replace(old_unix_time, str(self.timestamp_unix))

    def shift(self, seconds):
        """
        The shift function takes a log entry and shifts the timestamp by a given number of seconds.
        The shift function is used to correct for timezone differences between the system that generated
        the logs and the system on which they are being analyzed.  The shift function also updates all other
        timestamps in the log entry, including timestamps in messages.
        
        :param self: Represent the instance of the class
        :param seconds: Shift the timestamp by a certain amount of seconds
        :return: Nothing
        
        """
        old_unix_time = str(self.timestamp_unix)
        self.timestamp_unix += seconds
        ts = unixtime2apttime(self.timestamp_unix)
        date, time = ts.split()
        year, month, day = date.split("-")
        month = months[int(month) - 1]
        self.timestamp = "{} {} {}".format(month, day, time)
        self.message.replace(old_unix_time, str(self.timestamp_unix))

    def writeback(self):
        """
        The writeback function takes the timestamp and message from a log entry,
        and returns them in a string format that is suitable for writing to an output file.
        
        
        :param self: Represent the instance of the class
        :return: A string in the format of &quot;timestamp message&quot;
        
        """
        output = "{} {}".format(self.timestamp, self.message)
        return output


def parseFile(logname, verbose):
    """
    The parseFile function takes a log file as input and returns a list of syslog_event objects.
        
    
    :param logname: Specify the log file to be parsed
    :param verbose: Determine if the user wants to see all of the output or not
    :return: A list of syslog_event objects
    
    """
    events = []

    try:
        file = openFile(logname, "r", verbose)
        lines = file.readlines()
        for line in lines:
            if (not line == ""):
                events.append(syslog_event(line))
        return events

    except OSError as e:
        writeStderr(f"{type(e)}: {e}")
        print(f"{type(e)}: {e}")
        return -1


def filter_events(events, timestamp, message):
    """
    The filter_events function takes a list of events, and returns two lists:
        1. A list of all the events that match the given timestamp and message
        2. A list of all the events that do not match
    
    :param events: Store the events that are filtered out
    :param timestamp: Filter the events by timestamp
    :param message: Filter the events by message
    :return: A tuple of two lists
    
    """
    new_events = []
    old_events = []

    for event in events:
        if (timestamp is None or event.timestamp == timestamp) and (
                message is None or event.message.__contains__(message)):
            new_events.append(event)
        else:
            old_events.append(event)
    return (new_events, old_events)


def writeback2file(logfile, events, verbose=False):
    """
    The writeback2file function takes a logfile and an events list as input.
    It then opens the logfile for writing, and iterates through each event in the events list.
    For each event, it writes back to file using the writeback function of that particular event.
    
    :param logfile: Specify the file to be read from
    :param events: Pass the events list to the function
    :param verbose: Print out the file name
    :return: The file object
    
    """
    file = openFile(logfile, "w", verbose)

    for event in events:
        file.write(event.writeback())
        #file.write("\n")
    #file.write("\n")


def get_indexes_by_timestamp(data, target_timestamp, target_message):
    """
    The get_indexes_by_timestamp function takes in a list of objects, and returns the indexes of those objects
    that have a timestamp that matches the target_timestamp parameter. It also checks to see if the message attribute
    of each object contains the target_message string.
    
    :param data: Pass the data to the function
    :param target_timestamp: Filter the data by timestamp
    :param target_message: Filter the data by message
    :return: A list of indexes
    
    """
    return [index for index, item in enumerate(data) if
            item.timestamp == target_timestamp and item.message.__contains__(target_message)]


def year_generator_simple(parsedLogs, image_location, inode_number, partition_to_use, verbose=False):
    """
    The year_generator_simple function takes the parsed logs, image location, inode number and partition to use as input.
    It then extracts the inode data from the image using istat_extract_inode function. It then sets last modified year to be equal
    to first 4 characters of file modified time stamp (i.e., YYYY). It also initializes last month variable to 0 and reverses 
    the order of parsed logs list so that it can start from bottom up for assigning years. Then it iterates through each log entry 
    and assigns year based on following logic: if this is first log entry, assign
    
    :param parsedLogs: Pass the parsed logs to the function
    :param image_location: Pass the path to the image file
    :param inode_number: Get the last modified date of a file
    :param partition_to_use: Specify the partition to use
    :param verbose: Print out the output of the istat command
    :return: A list of parsedlogs, which are the logs with a year added
    
    """
    inode_data = istat_extract_inode(imagepath=image_location, inode_number=inode_number,
                                     offset=str(partition_to_use.start), verbose=verbose)
    last_modified = inode_data.file_modified
    last_modified_year = int(last_modified[0:4])
    last_month = 0
    parsedLogs.reverse()

    for i in range(len(parsedLogs)):
        if i == 0:
            parsedLogs[i].year = str(last_modified_year)
            last_month = months2[parsedLogs[i].timestamp[0:3]]
            parsedLogs[i].timestamp_unix = generate_epochtime(parsedLogs[i].timestamp, parsedLogs[i].year)
        else:
            this_month = months2[parsedLogs[i].timestamp[0:3]]
            if this_month > last_month:
                last_modified_year -= 1
            last_month = this_month
            parsedLogs[i].year = str(last_modified_year)
            parsedLogs[i].timestamp_unix = generate_epochtime(parsedLogs[i].timestamp, parsedLogs[i].year)
    parsedLogs.reverse()

    '''
    Einfach das Jahr nehmen aus den Metadaten
    Und dann von oben nach Unten durchgehen und beim Wechsel eines Jahres (NumMonatNeu > NumMonatAlt) Jahr um eins reduzieren
    '''
    return parsedLogs


def year_generator_complex(parsedLogs):
    """
    The year_generator_complex function is a function that takes in the parsed logs and returns the same parsed logs with
    the year field filled out. It does this by using the registrar.csv file, which contains all of the log entries from 
    UbuntuSyslog, to find any log entry that has a timestamp within one second of an entry in UbuntuSyslog. If it finds such 
    an entry, then it will use its year value to fill out the corresponding year value for each matching log entry.
    
    :param parsedLogs: Pass the parsed logs to the function
    :return: A list of parsedlogs with the year added to each log
    
    """
    commando.remove("./registrar.csv")

    commando.psteal("./UbuntuSyslog", "registrar.csv")
    commando.find_delete("plaso")

    csv_data = CSVParser.parse_csv("../../registrar.csv")

    for i in range(len(csv_data)):
        timestamp = ParseTimestamps.log2timeline_2log(csv_data[i]["datetime"])
        message = csv_data[i]["message"]
        closing_bracket = message.find(']')
        message = message[closing_bracket + 1:].strip()
        temp = get_indexes_by_timestamp(parsedLogs, timestamp[0], message)
        for j in range(len(temp)):
            parsedLogs[temp[j]].year = timestamp[1]
            parsedLogs[temp[j]].timestamp_unix = generate_epochtime(parsedLogs[temp[j]].timestamp,
                                                                    parsedLogs[temp[j]].year)
    return parsedLogs
