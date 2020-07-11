def third_z(table):
    import pandas as pd
    import numpy as np
    import statsmodels.formula.api as smf
    from scipy.stats import zscore
    import time


    data = table.copy()

    # Adding an outlier flag

    start_time = time.time()

    data[['case_z']] = data[['Case_Rate']].apply(zscore)
    data[['death_z']] = data[['Death_Rate']].apply(zscore)
    data[['service_z']] = data[['Percent_Food_Service']].apply(zscore)


    # Adding an outlier flag

    data['average'] = data[['case_z', 'death_z', 'service_z']].mean(axis=1)
    z_outliers = np.where((abs(data['average'])>= 3))
    z_out = data.loc[z_outliers]
    

    z_speed = ("--- %s seconds ---" % (time.time() - start_time))

    return z_out, z_speed
