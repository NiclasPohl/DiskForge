# date_and_time_2_unixtime()
The function `date_and_time_2_unixtime` converts a given date and time to a Unix timestamp.
## Parameters:
    def date_and_time_2_unixtime(date, time):
- date: The `date` parameter should be in the format 'YYYY-MM-DD'
- time: The `time` parameter should be in the format 'HH:MM:SS', where HH represents hours
    (00-23), MM represents minutes (00-59), and SS represents seconds (00-59). For example, '14:30:00'
    represents 2:30 PM
- **return:** The function `date_and_time_2_unixtime` takes a date and time in the format 'YYYY-MM-DD'
    and 'HH:MM:SS' respectively, converts it into a datetime object, and then returns the Unix timestamp
    (number of seconds since January 1, 1970) corresponding to that date and time.

## Workflow:
1. Format data and time to a datetime string
2. Create datetimeobject
3. Convert to int