import sqlite3
from Utility.Other.WriteTimeModLog import changedDBEntries


def db_update(filename, table, nval, where, operand, comparison_mode=None):
    changedDBEntries(db_query(filename, table, where, comparison_mode))
    con = sqlite3.connect(filename)
    cur = con.cursor()
    print(where)

    UPDATE = "UPDATE {}".format(table[0])
    SET = "SET {} {} {}".format(nval[0], operand, nval[1])
    if not where is None:
        WHERE = "WHERE "
        x = len(where)
        for i in range(0, x, 2):
            print(i)
            print(x)
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

    print(UPDATE_SQL_QUERY)

    cur.execute(UPDATE_SQL_QUERY)
    con.commit()
    cur.close()
    con.close()


def db_query(filename, table, where, comparison_mode=None):
    con = sqlite3.connect(filename)
    cur = con.cursor()

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

    cur.execute(SQL_QUERY)
    entries = cur.fetchall()

    return entries
