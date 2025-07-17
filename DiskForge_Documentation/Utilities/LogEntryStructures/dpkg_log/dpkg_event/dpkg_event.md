# class dpkg_event
The class `dpkg_event` is used to create an object which stores one event of the `dpkg.log`

It stores the values:
- timestamp: The timestamp of the event
- timestamp_unix: The `timestamp` converted to unixtime
- message: The rest of the event


The class object has the following functions:
- [\_\_init\_\_](./../../alternatives_log/alternatives_event/__init__.md)
- [\_\_lt\_\_](./../../alternatives_log/alternatives_event/__lt__.md)
- [change](./../../alternatives_log/alternatives_event/change.md)
- [shift](./../../alternatives_log/alternatives_event/shift.md)
- [writeback](./../../alternatives_log/alternatives_event/writeback.md)