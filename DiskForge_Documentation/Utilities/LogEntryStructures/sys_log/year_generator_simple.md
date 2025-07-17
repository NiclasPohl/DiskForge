# year_generator_simple()
The year_generator_simple function takes the parsed logs, image location, inode number and partition to use as input.
    It then extracts the inode data from the image using istat_extract_inode function. It then sets last modified year to be equal
    to first 4 characters of file modified time stamp (i.e., YYYY). It also initializes last month variable to 0 and reverses 
    the order of parsed logs list so that it can start from bottom up for assigning years. Then it iterates through each log entry 
    and assigns year based on following logic: if this is first log entry, assign year of file. For each other check if year skip and then give the corresponding year.
## Parameters:
    def year_generator_simple(parsedLogs, image_location, inode_number, partition_to_use, verbose=False):
- parsedLogs: Pass the parsed logs to the function
- image_location: Pass the path to the image file
- inode_number: Get the last modified date of a file
- partition_to_use: Specify the partition to use
- verbose: Print out the output of the istat command
- **return:** A list of parsedlogs, which are the logs with a year added
## Workflow:
1. `Last Year` is the year of the files modified timestamp
2. Reverse List of events
3. For each event:
   1. If first event:
      1. Event year = file year
   2. Else:
      1. If event_month > last_month:
         1. Year Skip
      2. Set Event year to last year
4. Reverse List