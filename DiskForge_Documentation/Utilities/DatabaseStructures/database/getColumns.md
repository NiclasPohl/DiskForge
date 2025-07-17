# getColumns()
The function `getColumns` retrieves the column names of a specified table in a SQLite database file.

## Parameters:
    def getColumns(filename, table):
-  filename: The `filename` parameter in the `getColumns` function is the name of the SQLite
    database file from which you want to retrieve column information
-  table: The `table` parameter in the `getColumns` function is the name of the table in the
    SQLite database from which you want to retrieve the column names
- **return:** The function `getColumns` returns a string containing the names of the columns in the
    specified table from the SQLite database file.

## Workflow:
1. Connect to database
2. Execute `PRAGMA table_info({table})`
3. Join columns