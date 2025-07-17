# compare2databases()
The function `compare2databases` compares entries between two SQLite databases based on specified
    columns and primary keys, returning rows with differences.
## Parameters:
    def compare2databases(file_new, file_old, table, changed_value_column, primary_key):
-  file_new: The `file_new` parameter is the file path to the new database that you want to
    compare with the old database. This function compares the data in the specified table between the
    new and old databases based on the provided parameters
-  file_old: The `file_old` parameter in the `compare2databases` function is the file path to
    the old version of the database that you want to compare with the new version. This parameter is
    used to attach the old database to the new one so that you can compare the entries between the two
    databases
-  table: The `table` parameter in the `compare2databases` function refers to the name of the
    table in the databases that you want to compare for differences
-  changed_value_column: The `changed_value_column` parameter in the `compare2databases`
    function represents the column in the specified table that is used to identify changes between the
    two databases. This column is used to compare values in the original and updated databases to
    determine if there are any differences
-  primary_key: The `primary_key` parameter in the `compare2databases` function is used to
    specify the column in the specified table that serves as the primary key for identifying unique rows
    in the database tables. It is used in the SQL query to join the original and updated tables based on
    this primary key and
- **return:** The function `compare2databases` returns a list of rows from the specified table that have
    differences in the specified column between the two databases.

## Workflow:
1. Attach both databases
2. Filter out entries which do not match
3. Return not matching entries