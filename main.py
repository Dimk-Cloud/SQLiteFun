import sqlite3
from contextlib import closing

import gendata
import sqlfuns

DEFAULT_DB_FNAME = gendata.DEFAULT_DB_FNAME
SQL_GET_SCHEMA = 'SELECT * FROM sqlite_schema'

# Creating a sample SQLite database with a single table holding
# categorized random values
#gendata.generate()

# A query to test a particular function
SQL_TEST = '''
    SELECT category, value,
    winmode(value) OVER(PARTITION BY category) agg_result
    FROM {table_name}
    ORDER BY category
'''

# Opening a DB connection to test the functions defined by classesin sqlfuns.py
with closing(sqlite3.connect(DEFAULT_DB_FNAME)) as conn:
    
    # Obtaining the name of the first table that comes along
    # Since there should be only one table, that's what we need.
    conn.row_factory = sqlite3.Row
    rows = conn.execute(SQL_GET_SCHEMA).fetchall()
    for row in rows:
        if row['type'] == 'table':
            table_name = row['tbl_name']
            break
    else:
        raise sqlite3.Error('There are no tables in the database')

    # Creating user-defined aggregate functions 
    conn.create_aggregate('geomean', 1, sqlfuns.GeoMean)
    conn.create_aggregate('harmomean', 1, sqlfuns.HarmoMean)
    conn.create_aggregate('mode', 1, sqlfuns.Mode)
    conn.create_aggregate('median', 1, sqlfuns.Median)
    conn.create_aggregate('stdev', 1, sqlfuns.StDev)
    conn.create_aggregate('variance', 1, sqlfuns.Variance)

    # Creating user-defined window (analytic) functions
    conn.create_window_function('wingeomean', 1, sqlfuns.WinGeoMean)
    conn.create_window_function('winharmomean', 1, sqlfuns.WinHarmoMean)
    conn.create_window_function('winmode', 1, sqlfuns.WinMode)
    conn.create_window_function('winmedian', 1, sqlfuns.WinMedian)
    conn.create_window_function('winstdev', 1, sqlfuns.WinStDev)
    conn.create_window_function('winvariance', 1, sqlfuns.WinVariance)

    # Issue your own SQL queries interactively at this point
    #breakpoint()

    # Executing the test SQL statement
    rows = conn.execute(SQL_TEST.format(table_name = table_name)).fetchall()

# Print out the result set   
for row in rows:
    for key in row.keys():
        print(row[key], end = '  ')
    print()

