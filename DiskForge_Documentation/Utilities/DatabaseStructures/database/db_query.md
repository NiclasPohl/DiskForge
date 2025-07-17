# db_query()
This Python function generates a SQL query based on the provided table name, conditions, and comparison mode.

## Parameters:
    def db_query(table, where, comparison_mode=None):
-  table: The `table` parameter in the `db_query` function is used to specify the name of the
    table from which you want to retrieve data. It is expected to be a list containing the name of the
    table as its first element
-  where: The `where` parameter in the `db_query` function is used to specify the conditions
    that records must meet to be included in the query results. It is a list that contains pairs of
    column names and values to be compared against
-  comparison_mode: The `comparison_mode` parameter in the `db_query` function is used to
    specify how the comparison should be done in the SQL query. It can take two values:
- **return:** The function `db_query` returns an SQL query based on the input parameters `table`,
    `where`, and `comparison_mode`. The SQL query is constructed to select all columns from the
    specified table and apply a WHERE clause based on the conditions provided in the `where` parameter.
    If `comparison_mode` is set to "strict", the WHERE clause uses strict equality comparisons,
    otherwise, it uses partial

## Workflow:
1. Build `SELECT * FROM ...` string
2. Parse `WHERE` parameters
3. Put all together to query