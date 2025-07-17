# update_database()
The function `update_database` updates a SQLite database with a given query and returns the entries
    that match the query.

## Parameters:
    def update_database(filename, query, update):
-  filename: The `filename` parameter in the `update_database` function is the name of the
    SQLite database file that you want to connect to and update
-  query: The `query` parameter in the `update_database` function is typically a SQL query that
    is used to filter and select specific entries from the database that need to be updated. It is used
    to retrieve the entries that match certain criteria specified in the query
-  update: The `update` parameter in the `update_database` function is a SQL query that is used
    to update the database entries based on the specified criteria. This query should be a valid SQL
    UPDATE statement that modifies the database records according to the conditions specified in the
    `query` parameter
- **return:** The function `update_database` returns the entries that match the query after updating the
    database with the provided update statement.

## Workflow:
1. Query database to get entries
2. Execute Update Query
3. Return entries