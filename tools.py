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


class LinearRegression(linear_model.LinearRegression):
    """
    LinearRegression class after sklearn's, but calculate t-statistics
    and p-values for model coefficients (betas).
    Additional attributes available after .fit()
    are `t` and `p` which are of the shape (y.shape[1], X.shape[1])
    which is (n_features, n_coefs)
    This class sets the intercept to 0 by default, since usually we include it
    in X.
    """

    def __init__(self, *args, **kwargs):
        if not "fit_intercept" in kwargs:
            kwargs['fit_intercept'] = False
        super(LinearRegression, self)\
                .__init__(*args, **kwargs)

    def fit(self, X, y, n_jobs=1):
        self = super(LinearRegression, self).fit(X, y, n_jobs)

        sse = np.sum((self.predict(X) - y) ** 2, axis=0) / float(X.shape[0] - X.shape[1])
        # se = np.array([
        #     np.sqrt(np.diagonal(sse[i] * np.linalg.inv(np.dot(X.T, X))))
        #                                             for i in range(sse.shape[0])
        #             ])
        se = np.array([np.sqrt(np.diagonal(sse * np.linalg.inv(np.dot(X.T, X))))])

        self.t = self.coef_ / se
        self.p = 2 * (1 - stats.t.cdf(np.abs(self.t), y.shape[0] - X.shape[1]))
        return self