# time_to_hex()
This Python function converts a user-inputted date and time into a hexadecimal timestamp.
## Parameters:
    def time_to_hex(usertime=None, verbose=False):
- :param usertime: It looks like the `usertime` parameter is used to take input from the user in the
    format "YYYY-MM-DD hh:mm:ss.microseconds". This input is then split into its individual components
    (year, month, day, hour, minute, second, microsecond) to create a datetime object
- :param verbose: The `verbose` parameter in the `time_to_hex` function is used to determine whether
    additional information and debugging messages should be printed during the execution of the
    function. When `verbose` is set to `True`, extra information such as the Python date & time
    representation and the hexadecimal conversion result will be, defaults to False (optional)
- **return:** The function `time_to_hex` returns a tuple containing two values:
    1. A hexadecimal string representing the Unix timestamp of the input date and time after conversion.
    2. A byte string representing the microseconds of the input time, converted to little-endian format.
   
## Workflow:
1. Split userinput
2. Parse splittet userinput
3. Fill up not given information
4. Shift Microseconds
5. Return