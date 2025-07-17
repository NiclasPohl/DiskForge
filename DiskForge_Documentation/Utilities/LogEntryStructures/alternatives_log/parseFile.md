# parseFile()
Function to parse the log file and create event objects
## Parameters:
    def parseFile(logname, verbose):
- logname: Filename and Path of the logfile
- verbose: Verbosity setting
- **return:** List of log entry events
## Workflow:
1. Split logfile in lines
2. Create for each line/lines new event object