# parse_timestamp2()
The parse_timestamp2 function takes a string timestamp and returns a datetime object.
        The function is used to convert the timestamps in the log file into datetime objects, which are easier to work with.
        The function uses strptime() from the datetime module, which converts strings into date/time objects based on format codes.
## Parameters:
    def parse_timestamp2(timestamp_str):

- timestamp_str: Pass in the string that we want to convert into a datetime object
- **return:** A datetime object

## Workflow:

    return datetime.strptime(timestamp_str, '%b %d %H:%M:%S')
