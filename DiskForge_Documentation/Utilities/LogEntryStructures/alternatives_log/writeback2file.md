# writeback2file()
Function to write back the event objects into the file
## Parameters:
    def writeback2file(logfile, events,verbose):
- logfile: Filename and Path of the logfile
- events: List of events that should be written back
- verbose: Verbosity setting
- **return:**
## Workflow:
1. Open File
2. For each event
   1. Write to file