import pandas as pd
from sklearn import preprocessing
import os 
import dateutil
import numpy as np
import matplotlib.pyplot as plt
import re

def read_csv(file_path):
    #type: str -> DataFrame
    assert os.path.exists(file_path), 'Path {} does not exists'.format(file_path)

    df = pd.read_csv(file_path)
    return df

def save_csv(df, file_name):
    #type: DataFrame, str -> None
    df.to_csv(file_name, sep='\t')

def remove_columns(df, columns):
    #type: DataFrame, [str] -> DataFrame
    df = df.drop(columns=columns)
    return df

def replace_with_nan(df, elements_to_replace):
    #type: DataFrame, [str] -> DataFrame
    df = df.replace(elements_to_replace,np.NaN)
    return df

def get_nan_stats(df):
    #type: DataFrame -> None
    for column in df.columns:
        n_na = df[column].isna().sum()
        total = len(df[column])
        na_per_total = n_na * 100 / total
        print('{}: {:0.2f}% ({}/{})'.format(column, na_per_total, n_na, total))

def encode_categorical(df):
    #type: DataFrame -> DataFrame
    df = pd.get_dummies(df, columns=df.select_dtypes(include=['category']).columns)
    return df

def fill_with_mean(df, columns):
    #type: DataFrame, [str] -> None
    for column in columns:
        df[column].fillna(df[column].mean(), inplace=True)

def fill_with_frequent(df, columns):
    #type: DataFrame, [str] -> None
    for column in columns:
        df[column].fillna(df[column].value_counts().argmax(), inplace=True)

def fill_ffill(df, columns):
    #type: DataFrame, [str] -> None
    for column in columns:
        df[column].fillna(method='ffill', inplace=True)

def get_timedate_delta(df, column_from, column_to):
    #type: DataFrame, str, str -> int
    return (df[column_from] - df[column_to]).dt.days

def extract_datetime_features(df):
    #type: DataFrame -> DataFrame
    for column in ['searched_date', 'departure_date', 'return_date']:
        df[column] = pd.to_datetime(df[column])
        df[column+'_month'] = df[column].dt.month.astype('category')
        df[column+'_day_of_week'] = df[column].dt.dayofweek.astype('category')

    df['search_dep_days'] = get_timedate_delta(df, 'departure_date', 'searched_date')
    df['return_dep_days'] = get_timedate_delta(df, 'return_date', 'departure_date')
    return df

def extract_unique_airlines_features(df):
    #type: DataFrame -> DataFrame
    score = []
    for row in df['unique_airlines']:
        row_ = re.findall(r"[\w*\w']+", row)
        score.append(len(row_))
    df['unique_airlines'] = pd.Series(score)
    return df


def get_data(df):
    df = read_csv('sample_searches.csv')

    df = remove_columns(df, ['country_code',  'region', 'city', 'number_of_children', 'number_of_seniors', 'number_of_adults'])

    df = replace_with_nan(df, ['-', '- '])

    df = extract_datetime_features(df)
    df = remove_columns(df, ['searched_date', 'departure_date', 'return_date'])

    df = extract_unique_airlines_features(df)

    category_columns = ["portal_id", "origin", "destination", "flight_class", "cheapest_engine"]
    for column in category_columns:
        df[column] = df[column].astype("category")
    fill_with_frequent(df, category_columns)

    numerical_columns = df.select_dtypes(include=['float', 'int'])
    fill_with_mean(df, numerical_columns)

    df = encode_categorical(df)

    min_max_scaler = preprocessing.MinMaxScaler()
    df = pd.DataFrame(min_max_scaler.fit_transform(df), columns=df.columns, index=df.index)

    return df

def correlation_matrix(df):
    from matplotlib import pyplot as plt
    from matplotlib import cm as cm

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    cmap = cm.get_cmap('jet', 30)
    cax = ax1.imshow(df.corr(), interpolation="nearest", cmap=cmap)
    ax1.grid(True)
    plt.title('Airline Feature Correlation')
    labels= df.columns
    ax1.set_xticklabels(labels,fontsize=6)
    ax1.set_yticklabels(labels,fontsize=6)
    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    fig.colorbar(cax, ticks=[.75,.8,.85,.90,.95,1])
    plt.show()
