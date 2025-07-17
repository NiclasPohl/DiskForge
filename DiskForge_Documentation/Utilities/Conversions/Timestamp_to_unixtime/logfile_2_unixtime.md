# logfile_2_unixtime()
The function `logfile_2_unixtime` converts a timestamp from a logfile event into Unix time based on
    the provided year.
## Parameters:
    def logfile_2_unixtime(year, timestamp):
- year: Year is the year in which the logfile event occurred. It is a numerical value
    representing the year (e.g., 2022)
- timestamp: The `timestamp` parameter should be in the format "MMM DD hh:mm:ss", where:
- **return:** The function `logfile_2_unixtime` returns the Unix time for the given year and timestamp
    provided as input.

## Workflow:
1. Split Timestamp
2. Lookup month in table
3. create datetime object
4. Use mktime to get unixtime