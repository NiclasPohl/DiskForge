# change()
This Python function generates SQL queries to select and update records in a table based on specified criteria.
## Parameters:
    def change(target_timestamp, target_url, new_ts, table, nval, where, comparison_mode):
-  **target_timestamp**: Target timestamp range to filter the URLs
-  **target_url**: The `target_url` parameter in the `change` function represents the URL that you
    want to target for the SQL query. It is used to filter the URLs in the database based on the URL
    pattern provided
-  **new_ts**: The `new_ts` parameter in the `change` function represents the new timestamp value
    that will be used to update the `last_visit_time` column in the `urls` table. This value will
    replace the existing timestamp within the specified bounds or conditions based on the other
    parameters provided to the function
-  **table**: Unused
-  **nval**: Unused
-  **where**: The `where` parameter in the `change` function is used to specify additional
    conditions for selecting and updating rows in the SQL queries. It allows you to further filter the
    rows based on specific criteria. The `where` parameter is used in the SQL queries to add conditions
    to the `SELECT` and
-  **comparison_mode**: Unused
- ****return:**** The function `change` returns a tuple containing two SQL queries. The first query is a
    SELECT statement to retrieve data from a table based on certain conditions, and the second query is
    an UPDATE statement to modify data in the same table based on the same conditions.

## Workflow:
1. Find out which filter parameters are given
2. Build SQL query with parameters