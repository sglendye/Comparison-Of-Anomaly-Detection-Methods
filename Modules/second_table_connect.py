def second_table(con):
    import pandas as pd
    import sqlite3

    table = pd.read_sql('''
    SELECT   a.fips
            ,b."Estimate!!RACE!!Total_population" AS Total_Pop
            ,CAST(a.cases AS float)/CAST(b."Estimate!!RACE!!Total_population" AS float) AS Case_Rate
            ,CAST(a.deaths AS float)/CAST(b."Estimate!!RACE!!Total_population" AS float) AS Death_Rate
    FROM Covid_Time_Series as a
    INNER JOIN Census_Age_Race as b
    ON a.fips = b.GEO_ID
    WHERE date = "7/3/2020" AND fips IS NOT NULL
    ''', con)

    return table
