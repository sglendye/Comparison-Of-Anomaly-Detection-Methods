def second_cook(table):
    import pandas as pd
    import numpy as np
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from statsmodels.formula.api import ols
    import time

    data = table.copy()

    start_time = time.time()

    model = smf.ols(formula='Case_Rate ~ Death_Rate + Percent_Food_Service', data=data).fit()
    cooks = model.get_influence()
    sm_fr = cooks.summary_frame()
    n = len(data.index)
    outlier = 4/n

    sm_fr.loc[(sm_fr.cooks_d >= outlier)] = 'T'
    high_cook = np.where((sm_fr['cooks_d']== 'T'))
    cook_out = data.loc[high_cook]

    cook_speed = ("--- %s seconds ---" % (time.time() - start_time))

    return cook_out, cook_speed
