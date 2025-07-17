# parse_timestamp1()
The parse_timestamp1 function takes a string timestamp and returns a datetime object.
    The function uses the strptime method to parse the string into a datetime object, then replaces the timezone info with UTC.

## Parameters:
    def parse_timestamp1(timestamp_str):
- timestamp_str: Pass the timestamp string to be parsed
- **return:** A datetime object with a timezone of utc

## Workflow:
    return datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)