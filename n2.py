"""
Code of Project-1 Network Backup Dataset
EE219 2017 Winter
Task 2: Linear regression of this model with cross validation

Zeyu Li
Jan 21, 2017

"""
import tools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

from sklearn import linear_model
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold



if __name__ == '__main__':
    # Manipulating the data
    input_file_name = "network_backup_dataset.csv"
    dataset = tools.read_data(input_file_name)
    categ_col = ['Day of Week', 'Work-Flow-ID', 'File Name']
    dataset = tools.encode_feature(dataset, categ_col)

    # y is the "Size of Backup (GB)"
    data_y = dataset['Size of Backup (GB)']
    data_X = dataset.drop('Size of Backup (GB)', axis=1)

    # Creating the object and do the Cross-validation
    kf = KFold(n_splits=10)
    for train, test in kf.split(data_X, data_y):
        X_train, X_test = data_X.ix[train,:], data_X.ix[test,:]
        y_train, y_test = data_y.ix[train], data_y.ix[test]
        # print train, test
        linear_regr = linear_model.LinearRegression()
        res = linear_regr.fit(X_train, y_train)
        print res
