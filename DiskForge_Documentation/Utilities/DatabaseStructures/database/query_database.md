# query_database()
The function `query_database` connects to a SQLite database, executes a query, fetches the results,
    and returns them.
## Parameters:
    def query_database(filename, query):
-  filename: The `filename` parameter in the `query_database` function is the name of the SQLite
    database file that you want to connect to and query data from. It should be a string that includes
    the path to the SQLite database file on your system
-  query: The `query` parameter in the `query_database` function is a SQL query that you want to
    execute on the database specified by the `filename` parameter. This query can be any valid SQL
    statement such as SELECT, INSERT, UPDATE, DELETE, etc., depending on what you want to achieve with
- **return:** The function `query_database` returns the result of the query executed on the database
    specified by the `filename`. The result is a list of tuples, where each tuple represents a row of
    the query result.

## Workflow:
1. Connect to database
2. Execute `query`
3. Fetch all entries
4. Return entries