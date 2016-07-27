import get_data
import process_data
import os
import pyodbc
import csv


def fetch_and_unzip():
    get_data.fetch_access_db()
    process_data.unzip()
    access_con = connect_access()


def connect_access(access_db=os.path.join(os.getcwd(), 'access_backup', 'Access.accdb')):
    """
    Connects to an access database.  Assumes that the machine has an Access driver:
    https://www.microsoft.com/en-pk/download/confirmation.aspx?id=13255

    Args:
        access_db: full path to the unzipped Access database.

    Returns:
        object: a pyodbc connection object.
    """
    driver_string = 'Microsoft Access Driver (*.mdb, *.accdb)'

    # connect to db
    con = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %(access_db))
    return con


def write_tables(access_con):
    """
    Takes a open access cursor.  Iterates over all the tables and views.  Writes a .csv for
    each view into a folder.

    Args:
        cursor: open pyodbc connection.  Output of connect_access().

    Returns:
        bool: True for success, False otherwise.
    """
    cur1 = access_con.cursor()
    cur2 = access_con.cursor()
    all_tables = cur1.tables(tableType='TABLE').fetchall()

    for table in all_tables:
        table_name = table.table_name
        print(table_name)
        cur2.execute("SELECT * FROM [%s]" % table_name)
        row = cur2.fetchone()
        if row:
            print(row)

        results = cur2.fetchall()
        if results:
            with open(table_name + '.csv', 'wb') as f:
                csv.writer(f, quoting=csv.QUOTE_NONE).writerows(results)

        # cursor.execute("SELECT * FROM %s" % table_name)
        # results = cursor.fetchone()
        # print(results)
        # for table_name in table_names:
        #     write_table(table_name.name)
        #
        # cursor.execute("SELECT * FROM %s" % table_name)

    # cur2.execute("SELECT * FROM Staff").fetchone()
    # cur2.execute("SELECT * FROM [%s]" % 'Class Count').fetchone()

if __name__ == '__main__':
    fetch_and_unzip()
