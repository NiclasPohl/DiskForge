# importing datetime module
import datetime
import time
import re

import datetime as datetime


def hexpadding(s):
    """
    The function `hexpadding` adds leading zeros to a hexadecimal string to ensure it is 8 characters
    long.
    
    :param s: The function `hexpadding` takes a hexadecimal string `s` as input and pads it with zeros
    to make it a total of 8 characters (excluding the '0x' prefix). The function then returns the padded
    hexadecimal string with the '0x' prefix
    :return: The function `hexpadding` takes a hexadecimal string `s` as input, adds '0x' to the
    beginning of the string, and then pads the string with zeros to make it a total length of 10
    characters (including '0x'). The function returns the modified hexadecimal string.
    """
    return '0x' + s[2:].zfill(8)


def time_to_hex(usertime=None, verbose=False):
    """
    This Python function converts a user-inputted date and time into a hexadecimal timestamp.
    
    :param usertime: It looks like the `usertime` parameter is used to take input from the user in the
    format "YYYY-MM-DD hh:mm:ss.microseconds". This input is then split into its individual components
    (year, month, day, hour, minute, second, microsecond) to create a datetime object
    :param verbose: The `verbose` parameter in the `time_to_hex` function is used to determine whether
    additional information and debugging messages should be printed during the execution of the
    function. When `verbose` is set to `True`, extra information such as the Python date & time
    representation and the hexadecimal conversion result will be, defaults to False (optional)
    :return: The function `time_to_hex` returns a tuple containing two values:
    1. A hexadecimal string representing the Unix timestamp of the input date and time after conversion.
    2. A byte string representing the microseconds of the input time, converted to little-endian format.
    """
    year, month, day, hour, minute, second, microsecond = 1970, 1, 1, 0, 0, 0, "000000000"
    print(f"Usertime: {usertime}")

    # userinput = input("Please Input the new Date and Time in the following format YYYY-MM-DD hh:mm:ss.mikroseconds ")
    userinput = re.split('[: -\._]', usertime)

    # TODO Hübscher machen von Timestamp eingabe
    # TODO Mikrosekundenpräzesion

    for i in range(7):
        if i >= len(userinput):
            break
        if len(userinput) == 1 and userinput[0] == '':
            userinput[0] = '1970'
            hour = 1
            second = 1  # TODO find out wieso dieser Bug
        else:
            match i:
                case 0:
                    year = userinput[i]
                case 1:
                    month = userinput[i]
                case 2:
                    day = userinput[i]
                case 3:
                    hour = userinput[i]
                case 4:
                    minute = userinput[i]
                case 5:
                    second = userinput[i]
                case 6:
                    microsecond = userinput[i]
                    # Auf die richtige Länger buffern
                    while len(microsecond) < 9:
                        microsecond += "0"

        # assigned regular string date
        # year, month, day, hour, minute, second, microsecond, and tzinfo

    # Shift by 2 Bit because only 30 Bit of the extra field are used for Nanoseconds and 2 Bit are used for extending the Date Timestamp
    microsecond = int(microsecond) * 4
    microsecond = microsecond.to_bytes(4, "little")

    date_time = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

    # print regular python date&time
    if verbose:
        print("\nDate Time: ", date_time)

    print("\nDate Time: ", date_time)
    print("\nDate Time: ", date_time)
    print("\nDate Time: ", date_time)
    print("\nDate Time: ", date_time)
    print("\nDate Time: ", date_time)
    print("\nDate Time: ", date_time)
    print("\nDate Time: ", date_time)
    print("\nDate Time: ", date_time)
    print("\nDate Time: ", date_time)
    print("\nDate Time: ", date_time)

    # displaying unix timestamp after conversion
    if verbose:
        print("Hex: ", hexpadding(hex(int((time.mktime(date_time.timetuple()))))))
    return (hexpadding(hex(int((time.mktime(date_time.timetuple()))))), microsecond)
    # This is for Converting hex to binary


def unixtime_to_hex(unixtime):
    """
    The function `unixtime_to_hex` converts a Unix timestamp to a hexadecimal representation with
    padding.
    
    :param unixtime: The `unixtime_to_hex` function takes a Unix timestamp as input and converts it to a
    hexadecimal representation with proper padding
    :return: The function `unixtime_to_hex` is returning the hexadecimal representation of the input
    `unixtime` after converting it to an integer. The `hexpadding` function is being called with the
    hexadecimal representation as an argument.
    """
    return hexpadding(hex(int(unixtime)))
