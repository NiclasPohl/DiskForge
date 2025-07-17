# shift()
The function `shift` generates SQL queries to select and update records in a database table based on
    specified criteria and a shift factor in seconds.

## Parameters:
    def shift(target_timestamp, target_url, shift_factor_seconds, table, nval, where, comparison_mode):
-  target_timestamp: The `target_timestamp` parameter is a tuple containing two elements
    representing the start and end timestamps for the query. It is used to filter records based on the
    `last_visit_date` field in the `moz_places` table
-  target_url: Target URL to search for in the database table. It is used as a filter condition
    in the SQL queries
-  shift_factor_seconds: The `shift_factor_seconds` parameter represents the number of seconds
    by which you want to shift the `last_visit_date` in the database table `moz_places`. This value is
    then converted to microseconds (`shift_factor_microseconds`) for the SQL query
-  table: Unused
-  nval: Unused
-  where: Unused
-  comparison_mode: Unused
- **return:** The function `shift` returns a tuple containing two SQL queries: `sql_query_bounds` and
    `sql_query_update`.

## Workflow:
1. Craft Queries depending on given parameters 