def first_z(table):
    import pandas as pd
    import numpy as np
    import statsmodels.formula.api as smf
    from scipy.stats import zscore
    import time


    # z-score test


    data = table.copy()

    # Timing the execution of this
    start_time = time.time()

    # Adding a column of z-scores
    data[['case_z']] = data[['cases1']].apply(zscore)

    #Slicing based on z-scores greater than 3 or less than -3
    z_outliers = np.where((data['case_z']>=3) | (data['case_z']<=-3))
    z_out = data.loc[z_outliers]
    

    z_speed = ("--- %s seconds ---" % (time.time() - start_time))

    return z_out, z_speed
