# Database - Change

The Change module for the database events is in the file [DB_Change.py](https://faui1-gitlab.cs.fau.de/lena.voigt/diskforge/-/blob/main/DiskForge/Modules/Timestomping/BrowserDatabase/DB_Change.py).

It contains the function DB_Change which uses the following parameters:

    def DB_Change(image_location=None, file_location=None, partition_num=None, table=None, where=None, nval=None,
              comparison_mode=None, db_name=None, target_timestamp=None, target_url=None, new_ts=None,
              verbose=False, primary_key=None, update_val=False, args=None):

- image_location: The Path of the image file on the users computer
- file_location: The Path of the file inside the image file
- partition_num: The Partition Number of the file inside the image file
- target_timestamp: The Timestamp on which you want to match
- target_url: The target URL on which you want to match
- new_ts: The new timestamp you want to set
- verbose: Activate for more output
- Returns -1 on Error

Worflow:

1. Convert new_ts to mikroseconds
2. Set db_interface, changed_column, table and primary_key
3. Extract File & Create Copy
4. Query the Database und Update it
5. Find out which entries changed and what their new values are
6. Write Changed DB back