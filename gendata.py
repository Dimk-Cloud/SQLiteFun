import sqlite3
import argparse
from random import choices
from contextlib import closing

import sqlfuns

DEFAULT_CATEGORIES = ('A', 'B', 'C', 'D')
DEFAULT_VALUE_MIN = 1
DEFAULT_VALUE_MAX = 100
DEFAULT_DS_LENGTH = 100  # Dataset length, the number of rows
#DB_FNAME = ':memory:' # If you are not into persistency :-)
DEFAULT_DB_FNAME = 'dataset.db'
DEFAULT_TABLE_NAME = 'ds' # For "dataset"
DEFAULT_INDEX_NAME = 'idx_cat'

# Will also create an INDEX on the category column,
# now just for kicks, but I might need one later
SQL_SCHEMA = f'''
    DROP TABLE IF EXISTS "{DEFAULT_TABLE_NAME}";
    DROP INDEX IF EXISTS "{DEFAULT_INDEX_NAME}";
    CREATE TABLE "{DEFAULT_TABLE_NAME}" (
            "id"	INTEGER,
            "category"	TEXT NOT NULL,
            "value"	INTEGER NOT NULL,
            PRIMARY KEY("id") );
    CREATE INDEX "{DEFAULT_INDEX_NAME}" ON {DEFAULT_TABLE_NAME}(category);
    '''

# This query will populate the table with random data
SQL_INSERT_DATA = f'INSERT INTO {DEFAULT_TABLE_NAME}(category, value) VALUES (?, ?)'

# Tracing errors in user-defined functions won't hurt
sqlite3.enable_callback_tracebacks(True)

def generate(categories = DEFAULT_CATEGORIES,
             value_min = DEFAULT_VALUE_MIN,
             value_max = DEFAULT_VALUE_MAX,
             ds_length = DEFAULT_DS_LENGTH,
             db_fname = DEFAULT_DB_FNAME,
             table_name = DEFAULT_TABLE_NAME
             ) -> int:
    """ Creates a small SQLite database with a single table table containing
        random categorized integer data values.

        The arguments:

        - categories: a sequence listing categories
        - value_min, value_max: the boundaries for the random integer values
        - ds_length: the number of the table's rows
        - db_fname: the file containing the SQLite database
        - table_name: the name of the table

        The function returns the number of rows added to the table"""

    # Randomly generating categories and values
    category_column = choices(categories, k = ds_length)
    values_column = choices(range(value_min, value_max+1), k = ds_length)

    # Creating and populating the database
    with closing(sqlite3.connect(db_fname)) as conn:
        conn.executescript(SQL_SCHEMA)
        rowcount = conn.executemany(
            SQL_INSERT_DATA,
            zip(category_column, values_column, strict=True)
            ).rowcount
        conn.commit()

    return rowcount

# Command-line interface
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        prog = 'gendata',
        description = 'Creates a simple SQLite database with a single table '
        'holding categorized random values',
        epilog = 'Thank you for using the program.'
        )

    parser.add_argument('-f', '--filename',
                        help = 'The name of the file containing the SQLite database. '
                        'If exists, the objects in it will be overwritten. '
                        f'Defaults to {DEFAULT_DB_FNAME}',
                        type = str,
                        default = DEFAULT_DB_FNAME,
                        required = False
                        )
    """ TBI
    parser.add_argument('-c', '--category_number',
                        help = 'The number of distinct categories to be randomly '
                        'chosen from when creating categorized random values '
                        f'Defaults to {DEFAULT_CATEGORIES}',
                        type = str,
                        default = DEFAULT_CATEGORIES,
                        required = False
                        )
    """
    
    args = parser.parse_args()

    generate(db_fname = args.filename)
             
    
    
    
                
    
    

























    
    

    




                     
