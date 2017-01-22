"""
Code of Project-1 Network Backup Dataset
EE219 2017 Winter

Zeyu Li
Jan 21, 2017

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def read_data():
    """
    Read the cvs dataset file and return a
    :return: Pandas dataframe of the csv file
    """
    dataset = pd.read_csv('network_backup_dataset.csv')

if __name__ == '__main__':
    read_data()