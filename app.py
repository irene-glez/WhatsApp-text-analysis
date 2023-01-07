import pandas as pd
import numpy as np
import streamlit as st
import regex as re
import matplotlib.pyplot as plt

import preprocess as prep
import stats_graphs as sts

MKL_NUM_THREADS=1
NUMEXPR_NUM_THREADS=1
OMP_NUM_THREADS=1

st.sidebar.title('Analiza tu chat de WhatsApp')

# uploading the file

uploaded_file = st.sidebar.file_uploader('Por favor, sube aquí el archivo .txt del chat')

if uploaded_file is not None:
    # extracting the text in bytes from file
    bytes_data = uploaded_file.getvalue()

    # transforming the bytes into text with decoder
    data = bytes_data.decode('utf-8')
 
    # preprocessing the text
    df = prep.preprocess(data)

    # displaying the dataframe
    # st.dataframe(df)

    # fetch unique users
    user_list = df['User'].unique().tolist()

    # removing the group notifications from users list and sort it
    user_list.remove('Group Notification')
    user_list.sort()

    # 'General' at the 0 position of the index, for showcasing the  overall chat group analysis by default
    user_list.insert(0, 'General')

    # 
    selected_user = st.sidebar.selectbox(
        'Elige un usuario y pulsa en "Mostrar análisis"', user_list)

    st.title('Análisis del chat') # de Whats App' + selected_user)
    if st.sidebar.button('Mostrar análisis'):

        # getting the stats of the selected user
        num_messages, num_words, media_omitted, links = sts.fetch_stats(
            selected_user, df)

        # we create 4 columns for the stats (messages, words, media and links)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Nº de mensajes')
            st.title(num_messages)

        with col2:
            st.header('Nº de palabras')
            st.title(num_words)

        with col3:
            st.header('Archivos enviados')
            st.title(media_omitted)

        with col4:
            st.header('Enlaces enviados')
            st.title(links)

        # activity of the users
        if selected_user == 'General':

            # dividing the space into two columns:
            # first one for a bar chart with the top 5 most active users and second one for a df with percentage of total activity 

            st.title('Actividad de los usuarios')
            activity_count, act_df = sts.fetch_activity_users(df)
            
            # two plots, one for each column
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(activity_count.index, activity_count.values, color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(act_df)

        # Word Cloud for selected user
        st.title('Nube de palabras')
        df_img = sts.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_img)
        st.pyplot(fig)

        # most common words in the chat
        most_common_df = sts.get_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Palabras más utilizadas')
        st.pyplot(fig)

        # Emoji Analysis
        emoji_df = sts.get_emoji_stats(selected_user, df)
        emoji_df.columns = ['Emoji', 'Total']

        st.title('Análisis de emojis')

        # col1, col2 = st.beta_columns(2)

        # # count
        # with col1:
        #     st.dataframe(emoji_df)
        # # percentage
        # with col2:
        emoji_count = list(emoji_df['Total'])
        perlist = [(i/sum(emoji_count))*100 for i in emoji_count]
        emoji_df['Porcentaje'] = np.array(perlist)
        st.dataframe(emoji_df)

        # Monthly timeline
        st.title('Actividad por mes')
        time = sts.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(time['Time'], time['Message'], color='blue')
        ax.tick_params(labelsize= 9)
        plt.xticks(fontsize= 9, rotation= 'vertical')
    
        plt.tight_layout()
        st.pyplot(fig)

        # Activity maps: days and months
        st.title('Mapas de actividad')

        col1, col2 = st.columns(2)

        with col1:

            st.header('Días de mayor actividad')

            days = sts.weekly_activity(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(days.index, days.values, color='purple')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)

        with col2:

            st.header('Meses de mayor actividad')
            months = sts.monthly_activity(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(months.index, months.values, color='orange')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)