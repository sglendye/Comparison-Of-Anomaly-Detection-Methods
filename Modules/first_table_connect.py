def first_table(con):
    import pandas as pd
    import sqlite3
    
    table = pd.read_sql('''
    SELECT fips, cases AS cases1, cases AS cases2
    FROM Covid_Time_Series
    WHERE date = "7/3/2020" AND fips IS NOT NULL
    ''', con)

    return table
