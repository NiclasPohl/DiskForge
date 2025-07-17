# get_indexes_by_timestamp()
The get_indexes_by_timestamp function takes in a list of objects, and returns the indexes of those objects
    that have a timestamp that matches the target_timestamp parameter. It also checks to see if the message attribute
    of each object contains the target_message string.
    The function is used by the complex year generation algorithm
## Parameters:
    def get_indexes_by_timestamp(data, target_timestamp, target_message):
- data: Pass the data to the function
- target_timestamp: Filter the data by timestamp
- target_message: Filter the data by message
- **return:** A list of indexes
## Workflow:
    return [index for index, item in enumerate(data) if
            item.timestamp == target_timestamp and item.message.__contains__(target_message)]
            