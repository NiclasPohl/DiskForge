# convert_istat_to_timestamp()
The convert_istat_to_timestamp function takes a string of the form
        &quot;YYYY-MM-DD HH:MM:SS.sss (TZ)&quot;
    and returns a datetime object localized to the given timezone TZ.
## Parameters:
    def convert_istat_to_timestamp(timestamp_str):
-  timestamp_str: Extract the timestamp and timezone information
- :return: A datetime object
## Workflow:
1. Split `timestamp_str`
2. Create datetime object
3. Localize datetime object