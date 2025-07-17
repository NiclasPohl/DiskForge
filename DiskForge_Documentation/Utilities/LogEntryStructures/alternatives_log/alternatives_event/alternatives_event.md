# class alternatives_event
The class `alternatives_event` is used to create an object which stores one event of the `alternatives.log

It stores the values:
- task: The task created the log entry
- timestamp: The timestamp of the event
- timestamp_unix: The event `timestamp` converted to unixtime
- message: The rest of the event

The class object has the following functions:
- [\_\_init\_\_](./__init__.md)
- [\_\_lt\_\_](./__lt__.md)
- [change](./change.md)
- [shift](./shift.md)
- [writeback](./writeback.md)