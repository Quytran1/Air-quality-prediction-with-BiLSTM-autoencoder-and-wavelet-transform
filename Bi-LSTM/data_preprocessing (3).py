import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing 


def read_data_csv(data_path):
    df=pd.read_csv(data_path)
    return df


def fill_missing_values(df):
    for column in df.columns:
        df[column] = df[column].interpolate()

    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)
    
    return df


def train_test_split(df):
    threshold = int(len(df)*0.8)
    train = df.iloc[:threshold]
    test = df.iloc[threshold:]
    
    # X_train = train.iloc[:,:-1]
    # y_train = train['AQI']
    # X_test = test.iloc[:,:-1]
    # y_test = test['AQI']

    X_train = train.iloc[:, :3]
    y_train = train['AQI']
    X_test = test.iloc[:, :3]
    y_test = test['AQI']

    y_train = np.reshape(y_train, (y_train.shape[0], 1))
    y_test = np.reshape(y_test, (y_test.shape[0], 1))
    
    return X_train, X_test, y_train, y_test


def scale_data(df_train, df_test, list_scale_features):
    scaler = MinMaxScaler(feature_range=(0, 1))
    values_train = df_train[list_scale_features].values
    scaled_values_train = scaler.fit_transform(values_train)
    df_train[list_scale_features] = scaled_values_train 
    
    values_test = df_test[list_scale_features].values
    scaled_values_test = scaler.transform(values_test)
    df_test[list_scale_features] = scaled_values_test

    return df_train, df_test


def window_slide(train,label):
    # drop dữ liệu dư
    window_size = 10
    X = []
    Y = []
    for i in range(window_size, len(train)):
        X.append(train[i-window_size:i,:])
        Y.append(label[i,:])
      
    return np.array(X), np.array(Y)