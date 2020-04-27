#! /usr/bin/env python
#  -*- coding: utf-8 -*-

'''
Anomaly Detection of GPS Spoofing Attacks on UAVs
Project Authors: Lior Pizman & Yehuda Pashay
GitHub: https://github.com/liorpizman/AnomalyDetection
DataSets: 1. ADS-B dataset 2. simulated data
Source code: https://github.com/esvhd/TimeSeriesRegressor
File created by: esvhd
---
Time Series Estimator wrapper for machine learning models
'''

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin, clone


class TimeSeriesEstimator(BaseEstimator):
    """
    Base Class for Time Series Estimators
    """

    def __init__(self, base_estimator, n_prev=3, n_ahead=1,
                 parallel_models=False, **base_params):
        self.base_estimator = base_estimator.set_params(**base_params)
        self.parallel_models = parallel_models
        self.n_prev = n_prev
        self.n_ahead = n_ahead
        self._fit_estimators = None
        self._is_autocor = None

    def __repr__(self):
        return "TimeSeriesEstimator: " + repr(self.base_estimator)

    def _window_dataset(self, n_prev, dataX, dataY=None, n_ahead=1):
        """
        converts a dataset into an autocorrelation dataset with number
        previous time steps = n_prev
        returns a an X dataset of shape (samples, timesteps, features) and
        a Y dataset of shape (samples,features)
        """
        is_pandas = isinstance(dataX, pd.DataFrame)

        if dataY is not None:
            # assert (type(dataX) is type(dataY))
            # TODO find way to still perform this check
            assert (len(dataX) == len(dataY))

        dlistX, dlistY = [], []
        for i in range(len(dataX) - n_prev + 1 - n_ahead):
            if is_pandas:
                dlistX.append(dataX.iloc[i:i + n_prev].as_matrix())
                if dataY is not None:
                    dlistY.append(
                        dataY.iloc[i + n_prev - 1 + n_ahead].as_matrix())
                else:
                    dlistY.append(
                        dataX.iloc[i + n_prev - 1 + n_ahead].as_matrix())
            else:
                dlistX.append(dataX[i:i + n_prev])
                if dataY is not None:
                    dlistY.append(dataY[i + n_prev - 1 + n_ahead])
                else:
                    dlistY.append(dataX[i + n_prev - 1 + n_ahead])

        darrX = np.array(dlistX)
        darrY = np.array(dlistY)
        return darrX, darrY

    def _unravel_window_data(self, data):
        """
        converts a dataset of shape (samples, timesteps, features) to a dataset
        of shape (samples,timesteps*features)
        """
        dlist = []
        one_dim = True if len(data.shape) == 2 else False
        for i in range(data.shape[0]):
            if one_dim:
                dlist.append(data[i, :].ravel())
            else:
                dlist.append(data[i, :, :].ravel())
        return np.array(dlist)

    def _preprocess(self, X, Y):
        '''
        Converts the data into a format so that it can be fed into any sklearn
        regressor
        :param X:
        :param Y:
        :return:
        '''
        X_wind, Y_data = self._window_dataset(self.n_prev, X, Y, self.n_ahead)
        X_data = self._unravel_window_data(X_wind)
        return X_data, Y_data

    def fit(self, X, Y=None):
        '''
        X and Y are datasets in chronological order, or X is a time series.
        '''

        self._is_autocor = True if Y is None else False

        X_data, Y_data = self._preprocess(X, Y)

        if self.parallel_models and len(Y_data.shape) > 1 and \
                Y_data.shape[1] > 1:
            self._fit_estimators = [clone(self.base_estimator)
                                    for i in range(Y_data.shape[1])]
            for i, estimator in enumerate(self._fit_estimators):
                estimator.fit(X_data, Y_data[:, i])
        else:
            self.base_estimator.fit(X_data, Y_data)

        return self


class TimeSeriesRegressor(TimeSeriesEstimator, RegressorMixin):
    """
    A wrapper object for any scikit learn regressor. This object is designed
    to turn any regressor into a time series regressor.

    """

    def predict(self, X, preprocessed=False):
        if not preprocessed:
            X_new = self._preprocess(X, Y=None)[0]
        else:
            X_new = X

        if self._fit_estimators is not None:
            results = []
            for estimator in self._fit_estimators:
                results.append(estimator.predict(X_new))
            return np.transpose(np.array(results))
        else:
            return self.base_estimator.predict(X_new)


def cascade_cv(n, n_folds, data_size=.8, test_size=.15, number=False):
    '''
    Splits the dataset into n_folds of overlapping but temporally contiguous
    data.
    :param n: the size of the dataset
    :param n_folds: number of train, test pairs to generate
    :param data_size: the proportion of data used in each train,test pair
    :param test_size: the relative size of each testing dataset
    :return:
    '''
    pairs = []
    shift = int(round((1 - data_size) * n / float(n_folds)))
    if shift < 4:
        raise (UserWarning("Small Shift warning: Consider less folds, "
                           "or a smaller data size"))
    for i in range(n_folds):
        start = shift * i
        end = min(start + int(data_size * n), n)

        if test_size <= 1 and not number:
            # line below from master branch but seem to be breaking the code
            # filed issue on github.
            # ntrn = int(n * (1 - test_size))
            ntrn = int((end - start) * (1 - test_size))
        elif test_size > 1 and number:
            ntrn = int(n * data_size - test_size)
        else:
            raise ValueError(
                "test_size: (frac or Int) and number:(True or False) "
                "should be set correctly")

        pairs.append((list(range(start, start + ntrn)),
                      list(range(start + ntrn, end))))
    return pairs
