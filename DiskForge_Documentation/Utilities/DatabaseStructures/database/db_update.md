# db_update()
This Python function generates an SQL UPDATE query based on the provided table, new values, conditions, and comparison mode.

## Parameters:
    def db_update(table, nval, where, operand, comparison_mode=None):
-  table: The `table` parameter in the `db_update` function represents the name of the database
    table that you want to update
-  nval: The `nval` parameter in the `db_update` function represents the new value that you want
    to update in the database table. It is a list containing two elements: the column name and the new
    value to be set in that column
-  where: The `where` parameter in the `db_update` function is used to specify the condition(s)
    that determine which records in the database table will be updated. It is a list that contains pairs
    of column names and values that are used in the WHERE clause of the SQL UPDATE statement
-  operand: The `operand` parameter in the `db_update` function represents the operation to be
    performed in the `SET` clause of an SQL `UPDATE` statement. It could be an operator like `=`, `+`,
    `-`, `*`, `/`, etc., depending on the specific update operation you
-  comparison_mode: The `comparison_mode` parameter in the `db_update` function is used to
    specify the type of comparison to be used in the WHERE clause of the SQL query. It can have two
    possible values:
- **return:** The function `db_update` returns an SQL query string for updating a database table. The
    query includes the UPDATE statement with the specified table name, the SET statement with the new
    value and operand, and the WHERE clause with the specified conditions based on the where, operand,
    and comparison_mode parameters.

## Workflow:
1. Craft `UPDATE` and `SET` strings
2. Parse all `WHERE` parameters
3. Put all together to query