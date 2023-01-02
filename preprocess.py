import streamlit as st
import pandas as pd
import numpy as np
import regex as re
import seaborn as sn


# function to separate time and date
def get_time_date(string):
    string = string.split(',')
    date, time = string[0], string[1]
    time = time.split('-')
    time = time[0].strip()

    return date+" "+time

# removing '\n' from the 'Message' column
def get_string(text):
    return text.split('\n')[0]

# final preprocessing function
def preprocess(data):
    # splitting date, time and dash at the start of every line of text
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    
    # separate dates from messages
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # put both in a dataframe
    df = pd.DataFrame({'user_messages': messages,
                       'message_date': dates})
        
    df['message_date'] = df['message_date'].apply(
        lambda text: get_time_date(text))
    df.rename(columns={'message_date': 'Date'}, inplace=True)

    # separation of the usernamane
    users = []
    messages = []

    for message in df['user_messages']:

        entry = re.split('([\w\W]+?):\s', message) # extracting the username
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])

        else:
            users.append('Group Notification') # the group's notifications don't have linked messages
            messages.append(entry[0])

    df['User'] = users
    df['Message'] = messages

    df['Message'] = df['Message'].apply(lambda text: get_string(text))
    df = df.drop(['user_messages'], axis=1)

    #df = df[['Message', 'Date', 'User']]

    # df = df.rename(columns={
    #                 'date': 'Date'})

    # splitting and type transformation  for all the info contained in the 'date' column with datetime:

    # df['Only date'] = pd.to_datetime(df['Date']).dt.date
    # df['Year'] = pd.to_datetime(df['Date']).dt.year
    # df['Month_num'] = pd.to_datetime(df['Date']).dt.month
    # df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
    # df['Day'] = pd.to_datetime(df['Date']).dt.day
    # df['Day_name'] = pd.to_datetime(df['Date']).dt.day_name()
    # df['Hour'] = pd.to_datetime(df['Date']).dt.hour
    # df['Minute'] = pd.to_datetime(df['Date']).dt.minute

    # return df
