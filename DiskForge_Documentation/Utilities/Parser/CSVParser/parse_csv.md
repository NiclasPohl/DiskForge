# parse_csv()
The parse_csv function takes a file path as an argument and returns the parsed data.
## Parameters:
    def parse_csv(file_path):
- file_path: Specify the path to the plaso file
- :return: A list of dictionaries
## Workflow:
1. Open csvfile
2. Read .csv file
3. Skip First Row
4. For each row:
   1. Fill in dictionary