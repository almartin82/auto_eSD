import get_data
import process_data
import os
import pyodbc
import csv
import pandas as pd


def fetch_and_unzip():
    get_data.fetch_access_db()
    process_data.unzip()
    access_con = connect_access()
    write_tables(access_con)
    access_con.close()


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


def write_tables(access_con, dest_folder='csvs'):
    """
    Takes a open access cursor.  Iterates over all the tables and views.  Writes a .csv for
    each view into a folder.

    Args:
        access_con: open pyodbc connection.  Output of connect_access().
        dest_folder: destination folder to write csv files

    Returns:
        bool: True for success, False otherwise.
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    cur = access_con.cursor()
    all_tables = cur.tables().fetchall()

    for table in all_tables:
        table_name = table.table_name
        table_type = table.table_type

        if table_type ==  'SYSTEM TABLE':
            continue

        print(table_name)

        # different SQL rules about ambiguous columns mean that some views can't be fetched
        # by sqlalchemy.
        try:
            df = pd.read_sql("SELECT * FROM [%s]" % table_name, access_con)
            file_name = table_type[:1].lower() + table_name
            df.to_csv(path_or_buf=os.path.join(dest_folder, "%s.csv" % file_name), index=False)
        except Exception as e:
            print(e)

    cur.close()
    return True

if __name__ == '__main__':
    fetch_and_unzip()
