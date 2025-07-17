# change()
The function `change` generates a database query and update statement based on input parameters.
## Parameters:
    def change(target_timestamp, target_url, new_ts, table, nval, where, comparison_mode):
-  target_timestamp: Unused
-  target_url: Unused
-  new_ts: Unused
-  table: The `table` parameter in the `change` function represents the name of the database
    table where the operation will be performed. It specifies the table in which the query and update
    operations will be executed
-  nval: The `nval` parameter in the `change` function represents the new value that you want to
    update in the database table. It is the value that will replace the existing value in the specified
    column of the table for the rows that meet the conditions specified in the `where` clause
-  where: The `where` parameter in the `change` function is used to specify the condition that
    must be met for the update operation to be applied to the database table. It is typically a SQL
    WHERE clause that filters the rows to be updated based on certain criteria. For example, `where="id=
-  comparison_mode: The `comparison_mode` parameter in the `change` function is used to specify
    how the comparison should be done in the database query and update operations. It could be values
    like "equal", "not equal", "greater than", "less than", etc., depending on the specific comparison
    logic needed for
- **return:** The function `change` is returning a tuple containing two database operations: a query and
    an update operation. The query operation is generated using the `db_query` function with parameters
    `table`, `where`, and `comparison_mode`. The update operation is generated using the `db_update`
    function with parameters `table`, `nval`, `where`, `operand`, and `comparison_mode`.

## Workflow:
1. Calls `db_query` to generate query
2. Calls `db_update` to generate update
3. Return tuple