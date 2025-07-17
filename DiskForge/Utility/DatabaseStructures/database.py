import sqlite3


def change(target_timestamp, target_url, new_ts, table, nval, where, comparison_mode):
    """
    The function `change` generates a database query and update statement based on input parameters.
    
    :param target_timestamp: Unused
    :param target_url: Unused
    :param new_ts: Unused
    :param table: The `table` parameter in the `change` function represents the name of the database
    table where the operation will be performed. It specifies the table in which the query and update
    operations will be executed
    :param nval: The `nval` parameter in the `change` function represents the new value that you want to
    update in the database table. It is the value that will replace the existing value in the specified
    column of the table for the rows that meet the conditions specified in the `where` clause
    :param where: The `where` parameter in the `change` function is used to specify the condition that
    must be met for the update operation to be applied to the database table. It is typically a SQL
    WHERE clause that filters the rows to be updated based on certain criteria. For example, `where="id=
    :param comparison_mode: The `comparison_mode` parameter in the `change` function is used to specify
    how the comparison should be done in the database query and update operations. It could be values
    like "equal", "not equal", "greater than", "less than", etc., depending on the specific comparison
    logic needed for
    :return: The function `change` is returning a tuple containing two database operations: a query and
    an update operation. The query operation is generated using the `db_query` function with parameters
    `table`, `where`, and `comparison_mode`. The update operation is generated using the `db_update`
    function with parameters `table`, `nval`, `where`, `operand`, and `comparison_mode`.
    """
    query = db_query(table=table, where=where, comparison_mode=comparison_mode)
    update = db_update(table=table, nval=nval, where=where, operand="=",
                       comparison_mode=comparison_mode)
    return (query, update)


def shift(target_timestamp, target_url, shift_factor_seconds, table, nval, where, comparison_mode):
    """
    The function `shift` generates database query and update statements based on input parameters.
    
    :param target_timestamp: Unused
    :param target_url: Unused
    :param shift_factor_seconds: The `shift_factor_seconds` parameter in the `shift` function represents
    the amount of time (in seconds) by which you want to shift the target timestamp. This parameter is
    used to calculate the new timestamp value based on the shift factor provided
    :param table: The `table` parameter in the `shift` function refers to the name of the database table
    on which the query and update operations will be performed. It specifies the table where the data is
    stored or from which data will be retrieved or updated
    :param nval: The `nval` parameter typically represents the value by which you want to update a
    specific column in a database table. In the context of the provided `shift` function, it seems to be
    used as the value to be added to the existing value in the specified column during an update
    operation
    :param where: The `where` parameter typically specifies the conditions that must be met for the
    query to return results or for the update to be applied. It is used to filter the data in the
    database table. The `where` parameter can include one or more conditions that must be satisfied for
    the query or update to
    :param comparison_mode: The `comparison_mode` parameter likely specifies how the comparison should
    be performed in the database queries. It could be used to determine whether the comparison should be
    for equality, greater than, less than, etc. The specific values that `comparison_mode` can take
    would depend on the implementation of the `db
    :return: The function `shift` is returning a tuple containing two database operations: a query and
    an update operation.
    """
    query = db_query(table=table, where=where, comparison_mode=comparison_mode)
    update = db_update(table=table, nval=nval, where=where, operand="+=",
                       comparison_mode=comparison_mode)
    return (query, update)


def db_update(table, nval, where, operand, comparison_mode=None):
    """
    This Python function generates an SQL UPDATE query based on the provided table, new values,
    conditions, and comparison mode.
    
    :param table: The `table` parameter in the `db_update` function represents the name of the database
    table that you want to update
    :param nval: The `nval` parameter in the `db_update` function represents the new value that you want
    to update in the database table. It is a list containing two elements: the column name and the new
    value to be set in that column
    :param where: The `where` parameter in the `db_update` function is used to specify the condition(s)
    that determine which records in the database table will be updated. It is a list that contains pairs
    of column names and values that are used in the WHERE clause of the SQL UPDATE statement
    :param operand: The `operand` parameter in the `db_update` function represents the operation to be
    performed in the `SET` clause of an SQL `UPDATE` statement. It could be an operator like `=`, `+`,
    `-`, `*`, `/`, etc., depending on the specific update operation you
    :param comparison_mode: The `comparison_mode` parameter in the `db_update` function is used to
    specify the type of comparison to be used in the WHERE clause of the SQL query. It can have two
    possible values:
    :return: The function `db_update` returns an SQL query string for updating a database table. The
    query includes the UPDATE statement with the specified table name, the SET statement with the new
    value and operand, and the WHERE clause with the specified conditions based on the where, operand,
    and comparison_mode parameters.
    """
    UPDATE = "UPDATE {}".format(table[0])
    SET = "SET {} {} {}".format(nval[0], operand, nval[1])
    if not where is None:
        WHERE = "WHERE "
        x = len(where)
        for i in range(0, x, 2):
            if i == x:
                break
            if not (i == 0):
                WHERE += " AND "
            if comparison_mode == "strict":
                where = "({} = '{}')".format(where[i], where[i + 1])
            else:
                where = "({} LIKE '%{}%')".format(where[i], where[i + 1])
            WHERE += where
            i = i + 1
        UPDATE_SQL_QUERY = "{} {} {}".format(UPDATE, SET, WHERE)
    else:
        UPDATE_SQL_QUERY = "{} {}".format(UPDATE, SET)

    return UPDATE_SQL_QUERY


def db_query(table, where, comparison_mode=None):
    """
    This Python function generates a SQL query based on the provided table name, conditions, and
    comparison mode.
    
    :param table: The `table` parameter in the `db_query` function is used to specify the name of the
    table from which you want to retrieve data. It is expected to be a list containing the name of the
    table as its first element
    :param where: The `where` parameter in the `db_query` function is used to specify the conditions
    that records must meet to be included in the query results. It is a list that contains pairs of
    column names and values to be compared against
    :param comparison_mode: The `comparison_mode` parameter in the `db_query` function is used to
    specify how the comparison should be done in the SQL query. It can take two values:
    :return: The function `db_query` returns an SQL query based on the input parameters `table`,
    `where`, and `comparison_mode`. The SQL query is constructed to select all columns from the
    specified table and apply a WHERE clause based on the conditions provided in the `where` parameter.
    If `comparison_mode` is set to "strict", the WHERE clause uses strict equality comparisons,
    otherwise, it uses partial
    """
    SELECT_FROM = "SELECT * FROM {}".format(table[0])
    if not where is None:
        WHERE = "WHERE "
        x = len(where)
        for i in range(0, x, 2):
            if not (i == 0):
                WHERE += "AND"
            if comparison_mode == "strict":
                where = "({} = '{}')".format(where[i], where[i + 1])
            else:
                where = "({} LIKE '%{}%')".format(where[i], where[i + 1])
            WHERE += where
        SQL_QUERY = "{} {}".format(SELECT_FROM, WHERE)
    else:
        SQL_QUERY = "{}".format(SELECT_FROM)

    return SQL_QUERY


def update_database(filename, query, update):
    """
    The function `update_database` updates a SQLite database with a given query and returns the entries
    that match the query.
    
    :param filename: The `filename` parameter in the `update_database` function is the name of the
    SQLite database file that you want to connect to and update
    :param query: The `query` parameter in the `update_database` function is typically a SQL query that
    is used to filter and select specific entries from the database that need to be updated. It is used
    to retrieve the entries that match certain criteria specified in the query
    :param update: The `update` parameter in the `update_database` function is a SQL query that is used
    to update the database entries based on the specified criteria. This query should be a valid SQL
    UPDATE statement that modifies the database records according to the conditions specified in the
    `query` parameter
    :return: The function `update_database` returns the entries that match the query after updating the
    database with the provided update statement.
    """
    entries = query_database(filename=filename, query=query)
    con = sqlite3.connect(filename)
    cur = con.execute(update)
    con.commit()
    cur.close()
    con.close()
    return entries


def query_database(filename, query):
    """
    The function `query_database` connects to a SQLite database, executes a query, fetches the results,
    and returns them.
    
    :param filename: The `filename` parameter in the `query_database` function is the name of the SQLite
    database file that you want to connect to and query data from. It should be a string that includes
    the path to the SQLite database file on your system
    :param query: The `query` parameter in the `query_database` function is a SQL query that you want to
    execute on the database specified by the `filename` parameter. This query can be any valid SQL
    statement such as SELECT, INSERT, UPDATE, DELETE, etc., depending on what you want to achieve with
    :return: The function `query_database` returns the result of the query executed on the database
    specified by the `filename`. The result is a list of tuples, where each tuple represents a row of
    the query result.
    """
    con = sqlite3.connect(filename)
    cur = con.cursor()
    cur.execute(query)
    entries = cur.fetchall()
    cur.close()
    con.close()
    return entries


def compare2databases(file_new, file_old, table, changed_value_column, primary_key):
    """
    The function `compare2databases` compares entries between two SQLite databases based on specified
    columns and primary keys, returning rows with differences.
    
    :param file_new: The `file_new` parameter is the file path to the new database that you want to
    compare with the old database. This function compares the data in the specified table between the
    new and old databases based on the provided parameters
    :param file_old: The `file_old` parameter in the `compare2databases` function is the file path to
    the old version of the database that you want to compare with the new version. This parameter is
    used to attach the old database to the new one so that you can compare the entries between the two
    databases
    :param table: The `table` parameter in the `compare2databases` function refers to the name of the
    table in the databases that you want to compare for differences
    :param changed_value_column: The `changed_value_column` parameter in the `compare2databases`
    function represents the column in the specified table that is used to identify changes between the
    two databases. This column is used to compare values in the original and updated databases to
    determine if there are any differences
    :param primary_key: The `primary_key` parameter in the `compare2databases` function is used to
    specify the column in the specified table that serves as the primary key for identifying unique rows
    in the database tables. It is used in the SQL query to join the original and updated tables based on
    this primary key and
    :return: The function `compare2databases` returns a list of rows from the specified table that have
    differences in the specified column between the two databases.
    """
    conn = sqlite3.connect(file_new)
    cursor = conn.cursor()

    # Attach the second database (the updated version)
    cursor.execute("ATTACH '{}' AS updated".format(file_old))

    # Compare the entries between the original and updated databases
    compare_query = """
        SELECT original.* 
        FROM {} original
        LEFT JOIN updated.{} updated ON original.{} = updated.{}
        WHERE original.{} != updated.{}
            OR updated.{} IS NULL
    """.format(table, table, primary_key, primary_key, changed_value_column, changed_value_column, primary_key)
    cursor.execute(compare_query)

    # Fetch all the rows that have differences
    different_entries = cursor.fetchall()

    # Detach the second database
    cursor.execute("DETACH updated")

    # Close the connection
    conn.close()
    return different_entries


def getColumns(filename, table):
    """
    The function `getColumns` retrieves the column names of a specified table in a SQLite database file.
    
    :param filename: The `filename` parameter in the `getColumns` function is the name of the SQLite
    database file from which you want to retrieve column information
    :param table: The `table` parameter in the `getColumns` function is the name of the table in the
    SQLite database from which you want to retrieve the column names
    :return: The function `getColumns` returns a string containing the names of the columns in the
    specified table from the SQLite database file.
    """
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    conn.close()
    column_names = [column[1] for column in columns]
    columns = ' | '.join(column_names)
    return columns
