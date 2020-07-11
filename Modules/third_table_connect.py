def third_table(con):
    import pandas as pd
    import sqlite3
    table = pd.read_sql('''
    SELECT   fips, Total_Pop, Case_Rate, Death_Rate, IFNULL(Percent_Food_Service, MIN(Percent_Food_Service)) AS Percent_Food_Service
    FROM(
    SELECT   a.fips
            ,b."Estimate!!RACE!!Total_population" AS Total_Pop
            ,CAST(a.cases AS float)/CAST(b."Estimate!!RACE!!Total_population" AS float) AS Case_Rate
            ,CAST(a.deaths AS float)/CAST(b."Estimate!!RACE!!Total_population" AS float) AS Death_Rate
            ,CAST(c."Estimate!!Total!!Civilian_employed_population_16_years_and_over!!Service_occupations!!Food_preparation_and_serving_related_occupations" AS float)
            /CAST(c."Estimate!!Total!!Civilian_employed_population_16_years_and_over" AS float) AS Percent_Food_Service
    FROM Covid_Time_Series as a
    INNER JOIN Census_Age_Race as b
    ON a.fips = b.GEO_ID
    INNER JOIN Census_Industry_Data as c
    ON b.GEO_ID = c.GEO_ID
    WHERE date = "7/3/2020" AND fips IS NOT NULL
    )

    UNION ALL

    SELECT   fips, Total_Pop, Case_Rate, Death_Rate, Percent_Food_Service
    FROM(
    SELECT   a.fips
            ,b."Estimate!!RACE!!Total_population" AS Total_Pop
            ,CAST(a.cases AS float)/CAST(b."Estimate!!RACE!!Total_population" AS float) AS Case_Rate
            ,CAST(a.deaths AS float)/CAST(b."Estimate!!RACE!!Total_population" AS float) AS Death_Rate
            ,CAST(c."Estimate!!Total!!Civilian_employed_population_16_years_and_over!!Service_occupations!!Food_preparation_and_serving_related_occupations" AS float)
            /CAST(c."Estimate!!Total!!Civilian_employed_population_16_years_and_over" AS float) AS Percent_Food_Service
    FROM Covid_Time_Series as a
    INNER JOIN Census_Age_Race as b
    ON a.fips = b.GEO_ID
    INNER JOIN Census_Industry_Data as c
    ON b.GEO_ID = c.GEO_ID
    WHERE date = "7/3/2020" AND fips IS NOT NULL AND Percent_Food_Service IS NOT NULL
    )
    ''', con)

    con.close()
    
    return table
