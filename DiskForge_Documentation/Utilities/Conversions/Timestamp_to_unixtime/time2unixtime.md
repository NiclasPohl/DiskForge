# time2unixtime()
The function `time2unixtime` converts a date object to a Unix timestamp.

## Parameters:
    def time2unixtime(dateobj):
- dateobj: The `dateobj` parameter in the `time2unixtime` function should be a string
    representing a date and time in the format 'YYYY-MM-DD HH:MM:SS'. For example, '2022-10-31 08:30:00'
- **return:** The function `time2unixtime` takes a date object in the format '%Y-%m-%d %H:%M:%S',
    converts it to a Unix timestamp (number of seconds since January 1, 1970), and returns the Unix
    timestamp as an integer.

## Workflow:
1. Convert timestamp object
2. Convert to int