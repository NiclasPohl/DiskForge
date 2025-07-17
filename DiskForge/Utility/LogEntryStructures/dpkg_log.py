from Utility.File_Operations.OpenFiles import openFile
from Utility.Conversions.Timestamp_to_unixtime import date_and_time_2_unixtime, unixtime2apttime, time2unixtime


class dpkg_event:
    timestamp = ""
    timestamp_unix = ""
    message = ""

    def __init__(self, line):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines what attributes it has.
        
        
        :param self: Represent the instance of the class
        :param line: Split the line into a list of strings
        :return: Nothing
        
        """
        line = line.split()
        self.timestamp = "{} {}".format(line[0], line[1])
        self.timestamp_unix = date_and_time_2_unixtime(line[0], line[1])
        self.message = ' '.join(line[2::])
        # print(self.message)

    def __lt__(self, other):
        """
        The __lt__ function is a special function that allows you to compare two objects of the same class.
        The __lt__ function returns True if self is less than other, and False otherwise.
        In this case, we are comparing two instances of the Flight class by their timestamp_unix attribute.
        
        :param self: Represent the instance of the class
        :param other: Compare the two objects
        :return: A boolean value
        
        """
        return self.timestamp_unix < other.timestamp_unix

    def change(self, new_ts):
        """
        The change function takes a new timestamp and changes the current
        timestamp to that. It also updates the unix time stamp.
        
        :param self: Represent the instance of the class
        :param new_ts: Change the timestamp of a given object
        :return: Nothing
        
        """
        self.timestamp = new_ts
        date, time = new_ts.split()
        self.timestamp_unix = date_and_time_2_unixtime(date, time)

    def shift(self, seconds):
        """
        The shift function takes a time in seconds and adds it to the timestamp_unix variable.
        It then converts that new unixtime into an apttime and stores it in the timestamp variable.
        
        :param self: Represent the instance of the class
        :param seconds: Shift the timestamp by a certain amount of seconds
        :return: Nothing
        
        """
        self.timestamp_unix += seconds
        self.timestamp = unixtime2apttime(self.timestamp_unix)

    def writeback(self):
        """
        The writeback function takes the timestamp and message from a log entry,
        and returns them in a string format that is suitable for writing to an output file.
        
        
        :param self: Refer to the object itself
        :return: A string that is formatted with the timestamp and message
        
        """
        output = "{} {}".format(self.timestamp, self.message)
        return output


def parseFile(logname, verbose):
    """
    The parseFile function takes a file name and returns a list of dpkg_event objects.
        
    
    :param logname: Specify the name of the file that is to be opened
    :param verbose: Print out the file name if it is not found
    :return: A list of dpkg_event objects
    
    """
    events = []

    file = openFile(logname, "r", verbose=verbose)
    lines = file.readlines()
    for line in lines:
        if (not line == ""):
            events.append(dpkg_event(line))
    return events


def filter_events(events, timestamp, message):
    """
    The filter_events function takes a list of events, a timestamp and a message as input.
    It returns two lists: The first one contains all events that match the given timestamp and/or message.
    The second one contains all other events.
    
    :param events: Filter the events
    :param timestamp: Filter events by timestamp
    :param message: Filter the events
    :return: A tuple of two lists
    
    """
    if not timestamp == None:
        unixtime = time2unixtime(timestamp)
    else:
        unixtime = None
    new_events = []
    old_events = []
    for event in events:
        if (unixtime is None or event.timestamp_unix == unixtime) and event.message.__contains__(message):
            # TODO check was event.message ist Entweder String oder Liste von Strings
            new_events.append(event)
        else:
            old_events.append(event)
    return (new_events, old_events)


def writeback2file(logfile, events, verbose):
    """
    The writeback2file function takes a logfile and an events list as input.
    It then opens the logfile for writing, and writes each event in the events list to it.
    
    
    :param logfile: Specify the file to read from
    :param events: Pass the events list to the function
    :param verbose: Print out the file name
    :return: Nothing
    
    """
    file = openFile(logfile, "w", verbose=verbose)

    for event in events:
        file.write(event.writeback())
        file.write("\n")
