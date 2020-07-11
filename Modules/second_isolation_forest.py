def second_forest(table):
    import pandas as pd
    import numpy as np
    import sklearn
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import IsolationForest
    import time
    import warnings

    data = table.copy()


    # Timing the forest execution
    start_time = time.time()

    to_model_columns = data.columns[2:4]
    clf=IsolationForest(n_estimators=1000, max_samples=100, contamination = .02, behaviour='new', random_state=42)
    clf.fit(data[to_model_columns])
    pred = clf.predict(data[to_model_columns])
    data['anomaly']=pred
    outliers=data.loc[data['anomaly']==-1]
    outlier_index=list(outliers.index)
    anomaly=data.loc[data['anomaly']==-1]

    forest_time = ("--- %s seconds ---" % (time.time() - start_time))

    return anomaly, forest_time
