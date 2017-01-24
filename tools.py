import pandas as pd
import numpy as np
from scipy import stats
from sklearn import linear_model

def read_data(file_name):
    """
    Read the cvs dataset file and return the dataframe of input data set
    :return: Pandas DataFrame of the data set csv file
    """
    dataset = pd.read_csv(file_name)
    return dataset

def encode_feature(dataframe, col_to_transform):
    """
    Encode the categorical features using OneHotEncoder,
    :param dataframe: The input dataset.
    :param col_to_transform: Name of columns that are categorical and should be transformed.
    :return: A new dataset with the columns transformed to encoded manner.
    """
    # Create a new data frame that are non-categorical
    all_col_names = list(dataframe.columns.values)
    non_categ_col = [item for item in all_col_names if item not in col_to_transform]
    new_df = dataframe.ix[:, non_categ_col]
    for col in col_to_transform:
        col_df = pd.get_dummies(dataframe[col], prefix=col)
        new_df = pd.concat([new_df, col_df], axis=1)
    return new_df
