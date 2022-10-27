# ==================================================
# Imports
import pandas as pd
import numpy as np


# ==================================================
# Functions
# Basic processing
def process_colname(df):
    container = []
    for i in df.columns.to_list():
        j = str(i).strip()
        k = (i, j)
        container.append(k)

    clean_names = {k:v for k, v in container}
    df = df.rename(clean_names, axis=1)
    return df


def process_string(df, column_list=None):
    if column_list is not None:
        for i in column_list:
            df[i] = df[i].str.strip()
                
    return df


def process_distribution(df, column_list=None):
    if column_list is not None:
        for i in column_list:
            df[i] = pd.to_numeric(df[i], downcast='integer')
    
    return df


def process_amount(df):
    #Remove undesirable characters
    df['amount'] = df['amount'].str.replace('$', '', regex=False)
    df['amount'] = df['amount'].str.replace(' ', '', regex=False)
    
    #Handle negative numbers in accounting format
    temp = []
    
    for i in df.itertuples():
        j = str(i[4])
        
        if '(' in j and ')' in j:
            j = j.replace('(', '')
            j = j.replace(')', '')
            j = '-' + j
            
        temp.append(j)
    
    df['amount'] = temp
    df['amount'] = pd.to_numeric(df['amount'])
    return df


def process_ignore(df, ignore_list=None):
    if ignore_list is not None:
        for colname in ignore_list:
            df = df.drop(colname, axis=1)
    
    return df

# Deep processing
def trunc_df(df, latest_id=None):
    #Truncate df if id exists
    if latest_id is not None:
        index = df.index[df['id'] == latest_id].to_list()[0] + 1
        df = df.truncate(before=index)
    
    return df


def format_labels(df, column_list=None):
    if column_list is not None:
        for colname in column_list:
            df[colname] = df[colname].str.lower()
            df[colname] = df[colname].str.replace("[@#$%^&*()']", '', regex=True)
            df[colname] = df[colname].str.replace('[-\s]', '_', regex=True)
            df[colname] = df[colname].str.replace('_{2,}', '_', regex=True)
            
    return df
