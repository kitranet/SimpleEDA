#!/usr/bin/env python
# coding: utf-8

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def remove_outlier(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return lower_bound, upper_bound

def find_specialchar(dataframe):
    for column in dataframe.columns:
        print(f"The unique values in {column} are as below\n", dataframe[column].unique())

def vif_cal(dataframe):
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    variables = dataframe.columns
    vif = pd.DataFrame()
    vif["VIF"] = [variance_inflation_factor(dataframe[variables].values, i) for i in range(dataframe[variables].shape[1])]
    vif["Features"] = variables
    return vif

def dups(dataframe):
    print(f'Number of duplicate rows = {dataframe.duplicated().sum()}')

def boxplt_continous(dataframe):
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set(style="whitegrid")
    for column in dataframe.select_dtypes(include=np.number).columns:
        plt.figure(figsize=(10, 5))
        sns.boxplot(x=dataframe[column])
        plt.title(f'Boxplot of {column}')
        plt.show()

def enhance_summary(dataframe, custom_percentiles=[]):
    # Summary for numerical columns
    numeric_summary = dataframe.describe(percentiles=[p/100 for p in custom_percentiles]).T
    numeric_summary['IQR'] = numeric_summary['75%'] - numeric_summary['25%']
    numeric_summary['LW'] = numeric_summary['25%'] - 1.5 * numeric_summary['IQR']
    numeric_summary['UW'] = numeric_summary['75%'] + 1.5 * numeric_summary['IQR']

    for column in dataframe.select_dtypes(include=np.number).columns:
        lower_range = numeric_summary.loc[column, 'LW']
        upper_range = numeric_summary.loc[column, 'UW']
        outliers = (dataframe[column] < lower_range) | (dataframe[column] > upper_range)
        num_outliers = np.sum(outliers)
        numeric_summary.loc[column, 'Outliers'] = num_outliers

    # Summary for categorical columns
    categorical_summary = dataframe.describe(include=['O']).T
    categorical_summary['Unique'] = dataframe.select_dtypes(include=['O']).nunique()
    categorical_summary['Top'] = dataframe.select_dtypes(include=['O']).mode().iloc[0]
    categorical_summary['Freq'] = dataframe.apply(lambda x: x.value_counts().iloc[0] if x.dtype == 'O' else np.nan)

    # Combine numerical and categorical summaries
    summary = pd.concat([numeric_summary, categorical_summary], axis=0, sort=False)
    
    # Add the number of duplicates and missing values
    for column in dataframe.columns:
        summary.loc[column, 'Duplicates'] = dataframe[column].duplicated().sum()
        summary.loc[column, 'Missing'] = dataframe[column].isnull().sum()

    # Add skewness column and skewness category column for numerical columns
    for column in dataframe.select_dtypes(include=np.number).columns:
        skew_value = dataframe[column].skew()
        summary.loc[column, 'Skew'] = round(skew_value, 2)

        if skew_value >= 1:
            summary.loc[column, 'Skew_Category'] = 'Positive'
        elif skew_value <= -1:
            summary.loc[column, 'Skew_Category'] = 'Negative'
        elif -0.5 <= skew_value <= 0.5:
            summary.loc[column, 'Skew_Category'] = 'Normal'
        else:
            summary.loc[column, 'Skew_Category'] = 'Undefined'

    return summary

# Example usage
if __name__ == "__main__":
    # Sample DataFrame
    data = {'A': [1, 2, 2, 4, 5, 6, 7, 8, 9, 10],
            'B': [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            'C': [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
            'D': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']}
    df = pd.DataFrame(data)

    # Enhanced summary
    summary = enhance_summary(df, custom_percentiles=[5, 95])
    print(summary)
