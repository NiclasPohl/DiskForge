# log2timeline_2log()
The log2timeline_2log function takes a string in the format of 'YYYY-MM-DDTHH:MM:SS' and converts it to a tuple containing
    the date in the format of 'Month DD YYYY HH:MM:SS' and the year as an integer. This is done so that we can use this function
    to sort our log2timeline data by date.
## Parameters:
    def log2timeline_2log(log2timeline):
- log2timeline: Convert the timestamp from the log file to a format that can be used in
- **return:** A tuple of two strings