# class dpkg_event
The class `dpkg_event` is used to create an object which stores one event of the `dpkg.log`

It stores the values:
- timestamp: Timestamp of the event
- year: Year of the event
- timestamp_unix: Unixtimestamp of the event
- message: Rest of the event
- audit: Flag if the audit parameter was found


The class object has the following functions:
- [\_\_init\_\_](./../../alternatives_log/alternatives_event/__init__.md)
- [\_\_lt\_\_](./../../alternatives_log/alternatives_event/__lt__.md)
- [change](./../../alternatives_log/alternatives_event/change.md)
- [shift](./../../alternatives_log/alternatives_event/shift.md)
- [writeback](./../../alternatives_log/alternatives_event/writeback.md)