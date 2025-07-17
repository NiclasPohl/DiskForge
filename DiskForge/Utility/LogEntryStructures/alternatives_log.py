from Utility.File_Operations.OpenFiles import openFile
from Utility.Conversions.Timestamp_to_unixtime import date_and_time_2_unixtime, unixtime2apttime, time2unixtime


# This Python class `alternatives_event` represents an event with task, timestamp, Unix timestamp, and
# message, and provides methods to compare timestamps, change timestamps, shift timestamps by seconds,
# and generate output.
class alternatives_event:
    task = ""
    timestamp = ""
    timestamp_unix = ""
    message = ""

    def __init__(self, line):
        """
        The function initializes an event object with attributes extracted from a line of text.
        
        :param line: The line of the log file event
        """
        line = line.split()
        self.task = line[0]
        self.timestamp = "{} {}".format(line[1], line[2][:-1])
        self.timestamp_unix = date_and_time_2_unixtime(line[1], line[2][:-1])
        self.message = ' '.join(line[3::])


    def __lt__(self, other):
        """
        Adding less then functionality for the struct
        :param other: The other event object
        :return:
        """
        return self.timestamp_unix < other.timestamp_unix

    def change(self, new_ts):
        """
        Functionality to change the timestamp of an event

        :param new_ts: The new timestamp that should be set
        :return:
        """
        self.timestamp = new_ts
        date, time = new_ts.split()
        self.timestamp_unix = date_and_time_2_unixtime(date, time)

    def shift(self, seconds):
        """
        Functionality to shift the timestamp of an event

        :param seconds: How many seconds should be shifted
        :return:
        """
        self.timestamp_unix += seconds
        self.timestamp = unixtime2apttime(self.timestamp_unix)

    def writeback(self):
        """
        Function for converting object back to string

        :return: Event String
        """
        output = "{} {}: {}".format(self.task, self.timestamp, self.message)
        return output


def parseFile(logname, verbose):
    """
    Function to parse the log file and create event objects

    :param logname: Filename and Path of the logfile
    :param verbose: Verbosity setting
    :return: List of log entry events
    """
    events = []

    file = openFile(logname, "r", verbose=verbose)

    lines = file.readlines()
    for line in lines:
        if (not line == ""):
            events.append(alternatives_event(line))
    return events


def filter_events(events, timestamp, message):
    """
    Function to filter events

    :param events: List of all events
    :param timestamp: Timestamp which should be filtered
    :param message: Message which should be filtered
    :return: Tuple of (filtered_events and rest)
    """
    if not timestamp == None:
        unixtime = time2unixtime(timestamp)
    else:
        unixtime = None
    new_events = []
    old_events = []
    for event in events:
        if (unixtime == None or event.timestamp_unix == unixtime) and event.message.__contains__(message):
            new_events.append(event)
        else:
            old_events.append(event)
    return (new_events, old_events)


def writeback2file(logfile, events,verbose):
    """
    Function to write back the event objects into the file

    :param logfile: Filename and Path of the logfile
    :param events: List of events that should be written back
    :param verbose: Verbosity setting
    :return:
    """
    file = openFile(logfile, "w", verbose=verbose)
    for event in events:
        file.write(event.writeback())
        file.write("\n")
