from Utility.File_Operations.OpenFiles import openFile
from Utility.Conversions.Timestamp_to_unixtime import date_and_time_2_unixtime, unixtime2apttime, \
    time2unixtime

'''
Wir können nun apt_history logs parsen
Das Datum shiften
Und es zurückschreiben lassen

Als nächstes brauchen wir einen Treiber Code
'''

sample_text = '''
Start-Date: 2024-01-03  12:27:53
Commandline: apt install sqlite3
Requested-By: niclas (1000)
Install: sqlite3:amd64 (3.37.2-2ubuntu0.1)
End-Date: 2024-01-03  12:27:54

Start-Date: 2024-01-05  17:03:32
Commandline: /usr/bin/unattended-upgrade
Upgrade: libsqlite3-0:amd64 (3.37.2-2ubuntu0.1, 3.37.2-2ubuntu0.3), sqlite3:amd64 (3.37.2-2ubuntu0.1, 3.37.2-2ubuntu0.3)
End-Date: 2024-01-05  17:03:32
'''


class apt_history_log_event:
    UnixTime_Start = None
    UnixTime_End = None
    TimeDiff = None

    Start_Date = None
    Commandline = None
    Requested_By = None
    Purge = None
    Hunspell_ptr_br = None
    Install = None
    Upgrade = None
    End_Date = None

    Middle = []

    def __init__(self, start, mess, end):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the object with all of its properties and methods.
        
        :param self: Represent the instance of the class
        :param start: Store the start date of a message (First Timestamp)
        :param mess: Store the middle part of the message, which is a string
        :param end: Store the end date of the message (Second Timestamp)
        :return: Nothing
        """
        self.Start_Date = start
        self.UnixTime_Start = date_and_time_2_unixtime(self.Start_Date.split()[1], self.Start_Date.split()[2])

        self.End_Date = end
        self.UnixTime_End = date_and_time_2_unixtime(self.End_Date.split()[1], self.End_Date.split()[2])

        self.Middle = mess

        self.TimeDiff = self.UnixTime_End - self.UnixTime_Start

    def __init2__(self, text):
        text = text.splitlines()
        for line in text:
            if line.__contains__("Start-Date:"):
                self.Start_Date = "{}\n".format(line)
                self.UnixTime_Start = date_and_time_2_unixtime(self.Start_Date.split()[1], self.Start_Date.split()[2])
            elif line.__contains__("End-Date"):
                self.End_Date = "{}\n".format(line)
                self.UnixTime_End = date_and_time_2_unixtime(self.End_Date.split()[1], self.End_Date.split()[2])
            else:
                self.Middle.append(line + "\n")
            '''elif line.__contains__("Commandline:"):
                self.Commandline = line
            elif line.__contains__("Requested-By:"):
                self.Requested_By = line
            elif line.__contains__("Install:"):
                self.Install = line 
        elif line.__contains__("Upgrade"):
            self.Upgrade = line
        elif line.__contains__("Purge:"):
            self.Purge = line
        elif line.__contains__("hunspell-pt-br:"):
            self.Hunspell_ptr_br = line
        elif line == "":
            continue
        else:
            print("Line {} does not meet any criteria".format(line)) '''

        self.TimeDiff = self.UnixTime_End - self.UnixTime_Start

    def __lt__(self, other):
        """
        The __lt__ function is used to compare two objects.
        The function returns True if the first object is less than the second object, and False otherwise.
        
        :param self: Refer to the current instance of the class, and is used to access variables that belongs to the class
        :param other: Compare the current object with another object
        :return: A boolean value
        """
        return self.UnixTime_Start < other.UnixTime_Start

    def change(self, new_ts):
        """
        The change function takes a new time and changes the start date of the appointment to that time.
        It also updates the end date accordingly.
        
        :param self: Represent the instance of the class
        :param new_ts: Change the time of the appointment
        :return: Nothing, but it does change the values of the start_date and end_date variables
        
        """
        new_ts = time2unixtime(new_ts)
        self.UnixTime_Start = new_ts
        self.UnixTime_End = self.UnixTime_Start + self.TimeDiff

        self.Start_Date = "Start-Date: {}".format(unixtime2apttime(self.UnixTime_Start).replace(" ", "  "))
        self.End_Date = "End-Date: {}".format(unixtime2apttime(self.UnixTime_End).replace(" ", "  "))

    def shift(self, seconds):
        """
        The shift function takes a number of seconds as an argument and adds that many seconds to the UnixTime_Start and UnixTime_End attributes.
        It then updates the Start-Date: and End-Date: lines in the .apt file accordingly.
        
        :param self: Represent the instance of the class
        :param seconds: Shift the start and end times by a certain amount of seconds
        :return: Nothing
        
        """
        self.UnixTime_Start += seconds
        self.UnixTime_End += seconds

        self.Start_Date = "Start-Date: {}\n".format(unixtime2apttime(self.UnixTime_Start).replace(" ", "  "))
        self.End_Date = "End-Date: {}\n".format(unixtime2apttime(self.UnixTime_End).replace(" ", "  "))

    def writeback(self):
        """
        The writeback function takes the values of the Start_Date, Middle, and End_Date
        attributes of a DateAndTime object and returns them as a string. The function is 
        used to write back to an .ics file after changes have been made.
        
        :param self: Refer to the object itself
        :return: A string of the date in the format:
        
        """
        values = [self.Start_Date, self.Middle, self.End_Date]
        output = ""
        for elem in range(len(values)):
            if values[elem] is not None:
                if (not elem == 1):
                    output += "{}".format(values[elem])
                else:
                    for i in range(len(self.Middle)):
                        output += "{}".format(values[elem][i])

        return output


def parseFile(logname, verbose):
    """
    The parseFile function takes a log file and parses it into a list of apt_history_log_event objects.
        
    
    :param logname: Specify the name of the file to be parsed
    :param verbose: Print out the information about the file being opened
    :return: A list of apt_history_log_event objects
    
    """
    events = []
    start = ""
    end = ""
    mess = []

    file = openFile(logname, "r", verbose=verbose)
    lines = file.readlines()
    for line in lines:
        if line == "\n":
            continue
        elif line.__contains__("Start-Date:"):
            start = line
        elif line.__contains__("End-Date:"):
            end = line
            events.append(apt_history_log_event(start, mess, end))
            mess = []
        else:
            mess.append(line)
    return events


def filter_events(events, timestamp, message):
    """
    The filter_events function takes in a list of events, a timestamp, and a message.
    It returns two lists: one containing all the events that match the timestamp and/or message
    and another containing all the events that do not match either.
    
    :param events: Pass the events to be filtered
    :param timestamp: Filter out events that do not have the same timestamp as the parameter
    :param message: Filter out events that do not contain the string in their message
    :return: Two lists
    
    """
    if not timestamp == None:
        unixtime = time2unixtime(timestamp)
    else:
        unixtime = None
    new_events = []
    old_events = []
    for event in events:
        if (unixtime == None or event.UnixTime_Start == unixtime) and any(message in s for s in event.Middle):
            new_events.append(event)
        else:
            old_events.append(event)
    return (new_events, old_events)


def writeback2file(logfile, events, verbose):
    """
    The writeback2file function takes a logfile and an events list as input.
    It then opens the logfile in write mode, and writes each event in the events list to it.
    
    
    :param logfile: Specify the file to write to
    :param events: Pass in the list of events
    :param verbose: Print out the file name if it is set to true
    :return: The file object
    
    """
    file = openFile(logfile, "w", verbose=verbose)

    file.write("\n")
    for event in events:
        file.write(event.writeback())
        file.write("\n")
