import pandas as pd
from collections import Counter
from wordcloud import WordCloud
from urlextract import URLExtract
# from nltk.corpus import stopwords
# import nltk
# nltk.download('stopwords')
import emoji



def fetch_stats(selected_user, df):

    # selecting a specific user
    if selected_user != 'General':
        df = df[df['User'] == selected_user]

    # number of messages
    num_messages = df.shape[0]

    # number of words
    words = []
    for message in df['Message']:
        words.extend(message.split())

    # number of shared media files 
    media_ommitted = df[df['Message'] == '<Media omitted>']

    # number of shared links 
    links = []
    extract = URLExtract()

    for message in df['Message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), media_ommitted.shape[0], len(links)


# activity by user
def fetch_activity_users(df):
    # top 5 most active users
    df = df[df['User'] != 'Group Notification']
    count = df['User'].value_counts().head()

    # percentage of total activity
    act_df = pd.DataFrame((df['User'].value_counts()/df.shape[0])*100)
    act_df = act_df.rename(columns= {'User' : "%"})
    return count, act_df

# Word Cloud
def create_wordcloud(selected_user, df):

    if selected_user != 'General':
        df = df[df['User'] == selected_user]
    
    # getting the stopwords

    file = open('spanish_stopwords.txt', 'r')
    stopwords = file.read()
    stopwords = stopwords.split('\n')
    
    # generate the cloud
    wc = WordCloud(stopwords= stopwords, max_words= 100, width=500, height=500,
                   min_font_size=12, background_color='black')
    # cut and concatenate the words from the 'Message' column
    df_wc = wc.generate(df['Message'].str.cat(sep=" "))

    return df_wc


# get the 20 most common words
def get_common_words(selected_user, df):

    # getting the stopwords

    file = open('spanish_stopwords.txt', 'r')
    stopwords = file.read()
    stopwords = stopwords.split('\n')

    if selected_user != 'General':
        df = df[df['User'] == selected_user]

    timeline = df[(df['User'] != 'Group Notification') | (df['User'] != '<Media omitted>')]

    words = []

    #emojis = []

    # for message in df['Message']:
    #     emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    #     for word in emojis:
    #         if word not in emojis:            
    #             words.append(word)
 

    for message in timeline['Message']:
        for word in message.lower().split():
            if word not in stopwords:            
                words.append(word)
                

    top_20_w = pd.DataFrame(Counter(words).most_common(20))
    return top_20_w

# get the most used emojis
def get_emoji_stats(selected_user, df):

    if selected_user != 'General':
        df = df[df['User'] == selected_user]

    emojis = []

    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

# user activity per month
def monthly_timeline(selected_user, df):

    if selected_user != 'General':
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['Year', 'Month_num', 'Month']).count()[
        'Message'].reset_index()

    # get month and year
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['Time'] = time

    return timeline

# activity per month
def monthly_activity(selected_user, df):

    if selected_user != 'General':
        df = df[df['User'] == selected_user]

    return df['Month'].value_counts()

# activity per week
def weekly_activity(selected_user, df):

    if selected_user != 'General':
        df = df[df['User'] == selected_user]

    return df['Day_name'].value_counts()