# class apt_history_log_event
The class `apt_history_log_event` is used to create an object which stores one event of the `apt/history.log

It stores the values:
- UnixTime_Start: Unixtime of the start timestamp
- UnixTime_End: Unixtime of the end timestamp
- TimeDiff: Difference between `UnixTime_Start` and `UnixTime_End`
- Start_Date: Start Timestamp
- End_Date: End Timestamp
- Middle: Rest of the Event


The class object has the following functions:
- [\_\_init\_\_](./../../alternatives_log/alternatives_event/__init__.md)
- [\_\_lt\_\_](./../../alternatives_log/alternatives_event/__lt__.md)
- [change](./../../alternatives_log/alternatives_event/change.md)
- [shift](./../../alternatives_log/alternatives_event/shift.md)
- [writeback](./../../alternatives_log/alternatives_event/writeback.md)