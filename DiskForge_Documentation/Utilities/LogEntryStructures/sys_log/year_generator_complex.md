# year_generator_complex()
The year_generator_complex function is a function that takes in the parsed logs and returns the same parsed logs with
    the year field filled out. It does this by using the registrar.csv file, which contains all of the log entries from 
    UbuntuSyslog, to find any log entry that has a timestamp within one second of an entry in UbuntuSyslog. The file is created using log2timeline. If it finds such 
    an entry, then it will use its year value to fill out the corresponding year value for each matching log entry.

## Parameter:
    def year_generator_complex(parsedLogs):
- parsedLogs: Pass the parsed logs to the function
- **return:** A list of parsedlogs with the year added to each log
## Workflow:
1. Run `psteal` for the logfile
2. Parse the resulting file
3. Match Parsed events to event list
4. Set Year for each event