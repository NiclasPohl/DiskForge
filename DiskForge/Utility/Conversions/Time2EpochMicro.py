from datetime import datetime
import pytz


def timestamp_to_epoch_micro_bounds(ts):
    """
    The function `timestamp_to_epoch_micro_bounds` converts a timestamp to a range of epoch timestamps
    in microseconds.
    
    :param ts: The `ts` parameter in the `timestamp_to_epoch_micro_bounds` function should be a string
    representing a timestamp in the format "YYYY-MM-DD HH:MM:SS"
    :return: The function `timestamp_to_epoch_micro_bounds` returns a tuple containing two values - the
    lower bound and upper bound of the timestamp converted to microseconds. The lower bound is the
    timestamp in microseconds and the upper bound is the next timestamp in microseconds minus 1.
    """
    timezone = pytz.timezone('UTC')
    timestamp_datetime = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S %Z").replace(tzinfo=timezone)  #
    unix_time_lower_bound = int(timestamp_datetime.timestamp())
    unix_time_upper_bound = unix_time_lower_bound + 1
    unix_time_lower_bound *= 1000000
    unix_time_upper_bound *= 1000000
    unix_time_upper_bound -= 1
    return (unix_time_lower_bound, unix_time_upper_bound)
