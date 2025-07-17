from datetime import datetime, timezone

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def parse_timestamp1(timestamp_str):
    """
    The parse_timestamp1 function takes a string timestamp and returns a datetime object.
    The function uses the strptime method to parse the string into a datetime object, then replaces the timezone info with UTC.
    
    :param timestamp_str: Pass the timestamp string to be parsed
    :return: A datetime object with a timezone of utc

    """
    return datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)


def parse_timestamp2(timestamp_str):
    """
    The parse_timestamp2 function takes a string timestamp and returns a datetime object.
        The function is used to convert the timestamps in the log file into datetime objects, which are easier to work with.
        The function uses strptime() from the datetime module, which converts strings into date/time objects based on format codes.
    
    :param timestamp_str: Pass in the string that we want to convert into a datetime object
    :return: A datetime object

    """
    return datetime.strptime(timestamp_str, '%b %d %H:%M:%S')


def match_log2log2timeline(log, log2timeline):
    """
    The match_log2log2timeline function takes two arguments:
        1. log - a string representing the date and time of an event in the logs, e.g., &quot;Apr  4 00:00:01&quot;
        2. log2timeline - a string representing the date and time of an event in the log2timeline output, e.g., &quot;2018-04-04T00:00&quot;
    
    :param log: Match the date and time of the log file to that of the timeline
    :param log2timeline: Find the date in the log file
    :return: A boolean value

    """
    timestamp_str3 = log2timeline[0:19]
    temp = timestamp_str3.split("-")
    temp2 = temp[2].split("T")
    temp3 = months[int(temp[1]) - 1]
    d = temp3 + " " + temp2[0] + " " + temp2[1]
    return d == log


def log2timeline_2log(log2timeline):
    """
    The log2timeline_2log function takes a string in the format of 'YYYY-MM-DDTHH:MM:SS' and converts it to a tuple containing
    the date in the format of 'Month DD YYYY HH:MM:SS' and the year as an integer. This is done so that we can use this function
    to sort our log2timeline data by date.
    
    :param log2timeline: Convert the timestamp from the log file to a format that can be used in
    :return: A tuple of two strings

    """
    timestamp_str3 = log2timeline[0:19]
    temp = timestamp_str3.split("-")
    temp2 = temp[2].split("T")
    temp3 = months[int(temp[1]) - 1]
    d = temp3 + " " + temp2[0] + " " + temp2[1]
    return (d, temp[0])


# Example usage
'''
timestamp_str1 = '2023-11-23T15:24:46.000000Z'
timestamp_str2 = 'Nov 23 15:24:46'
timestamp_str3 = timestamp_str1[0:19]
print(timestamp_str3)
temp = timestamp_str3.split("-")
print(temp)
temp2 = temp[2].split("T")
print(temp2)
temp3 = months[int(temp[1])-1]
print(int(temp[1])-1)
print(temp3)
d = temp3 + " " + temp2[0] + " " + temp2[1]
print(d)

print(timestamp_str2)
print(d == timestamp_str2)
# Parse timestamps
dt1 = parse_timestamp1(timestamp_str1)
dt2 = parse_timestamp2(timestamp_str2)

# Now, dt1 and dt2 are datetime objects, and you can compare or work with them as needed
#print(dt1)
#print(dt2)

# For example, to compare the two timestamps
if dt1 == dt2:
    print()
    #print("Timestamps match!")
else:
    print()
'''

# print(match_log2log2timeline('Nov 23 15:24:46','2023-11-23T15:24:46.000000Z'))
# print(log2timeline_2log("2023-11-23T15:24:46.000000Z"))
