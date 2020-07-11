# Writing our tables from the three different data files. This module doesa quick check on the database to see if the tables already exist.
# If they don't, it writes a new one for each file and adds an index to them to help speed up the merges in the second and third exercises.
# If a table does exist, it just passes over it and moves to the next one.
# This check is to allow the user to re-run the full procedure without it returning errors on the first step.

def write_tables(con, dir_path)
    import pandas as pd
    import sqlite3

    count = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' AND name='{Census_Age_Race}'", con)
    if len(count.index) == 0:
        data = pd.read_csv(dir_path+'\\'+'Data'+'\\'+'ACS_5yr_demo_data.csv')
        data.to_sql('Census_Age_Race', con, index=False)
        con.commit()
        sql = ("CREATE INDEX idx_age_race_fips ON Census_Age_Race (GEO_ID);")
        curs.execute(sql)
        con.commit()
    else:
        continue

    count = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' AND name='{Census_Industry_Data}'", con)
    if len(count.index) == 0:
        data = pd.read_csv(dir_path+'\\'+'Data'+'\\'+'ACS_5yr_industry_data.csv')
        data.to_sql('Census_Industry_Data', con, index=False)
        con.commit()
        sql = ("CREATE INDEX idx_industry_fips ON Census_Industry_Data (GEO_ID);")
        curs.execute(sql)
        con.commit()
    else:
        continue
    
    count = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' AND name='{Covid_Time_Series}'", con)
    if len(count.index) == 0:
        data = pd.read_csv(dir_path+'\\'+'Data'+'\\'+'NYT_historical_to_7_3.csv')
        data.to_sql('Covid_Time_Series', con, index=False)
        con.commit()
        sql = ("CREATE INDEX idx_covid_fips ON Covid_Time_Series (fips);")
        curs.execute(sql)
        con.commit()
    else:
        continue
    


