# shift()
This Python function shifts the last visit time of URLs in a database based on specified criteria.

## Parameters:
    def shift(target_timestamp, target_url, shift_factor_seconds, table, nval, where, comparison_mode):
-  target_timestamp: Target timestamp is a tuple containing two values representing the start
    and end timestamps for filtering the data in the SQL query. It is used to specify the time range for
    selecting and updating records in the database
-  target_url: The `target_url` parameter in the `shift` function represents the URL that you
    want to target for shifting the last visit time. This URL will be used in the SQL queries to filter
    the rows based on the URL pattern provided
-  shift_factor_seconds: The `shift_factor_seconds` parameter represents the amount of time in
    seconds by which you want to shift the `last_visit_time` in the database table. This value is used
    to calculate the shift factor in microseconds, which is then applied to update the `last_visit_time`
    values in the specified records
-  table: The `table` parameter in the `shift` function represents the name of the table in the
    database where the URLs are stored. This table is referenced in the SQL queries generated within the
    function to perform operations on the data within that table
-  nval: Unused
-  where: The `where` parameter in the `shift` function is used to specify additional conditions
    for selecting and updating rows in the SQL queries. It allows you to filter the rows based on
    specific criteria in the `WHERE` clause of the SQL statements. This parameter helps in narrowing
    down the selection of rows that
-  comparison_mode: Unused
- **return:** The function `shift` returns a tuple containing two SQL queries: `sql_query_bounds` and
    `sql_query_update`.

## Workflow:
1. Filter with given parameters
2. Build SQL Query with parameters