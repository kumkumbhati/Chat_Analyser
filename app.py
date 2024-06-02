import streamlit as st
import preprocess
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyser')

# For uploading the file
uploaded_file = st.sidebar.file_uploader('')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')

    df = preprocess.processing(data)

    # st.dataframe(df)

    # Getting the list of users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'overall')  # Insert 'overall' at index 0

    selected_user = st.sidebar.selectbox('Analysis with respect to...', user_list)

    if st.sidebar.button('Show Analyse'):
        st.title('Top Statistics')
        num_messages, words, num_media_msg, num_link = helper.fetch_stats(selected_user, df)

        # Use st.columns(4) to create four columns
        columns = st.columns(4)

        if len(columns) == 4:
            col1, col2, col3, col4 = columns
            with col1:
                st.header('Total Message')
                st.title(num_messages)

            with col2:
                st.header('Total Words')
                st.title(words)

            with col3:
                st.header('Media Shared')
                st.title(num_media_msg)

            with col4:
                st.header('links Shared')
                st.title(num_link)
        else:
            st.error("Error: Unable to create four columns.")



        #monthly timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user, df)
        if timeline is not None:
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='green')  # Use color instead of colour

            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        else:
            st.error("Error: Unable to generate timeline plot.")

        #daily timeline

        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user, df)
        if daily_timeline is not None:
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='yellow')  # Use color instead
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        else:
            st.error("Error: Unable to generate daily timeline plot.")


        #activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most Busy Day')
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index , busy_day.values, color = 'orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Month')
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index , busy_month.values, color = 'red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #heatmap
        u_heatmap = helper.activity_heatmap(selected_user, df)
        st.title('Activity Heatmap')
        fig, ax = plt.subplots()
        sns.heatmap(u_heatmap, ax=ax)
        st.pyplot(fig)





        # Finding the busiest personnel
        if selected_user == 'overall':
            # Use st.columns(2) to create two columns for the second half
            columns_second_half = st.columns(2)

            if len(columns_second_half) == 2:
                col1_second_half, col2_second_half = columns_second_half
                with col1_second_half:
                    st.title("Most Busy User")

                    x, new_df = helper.most_busy_user(df)
                    fig, ax = plt.subplots()

                    ax.bar(x.index, x.values, color='blue')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                with col2_second_half:
                    st.title("")
                    st.dataframe(new_df)
            else:
                st.error("Error: Unable to create two columns for the second half.")





            # wordcloud formation
            st.title("Wordcloud Visualization")
            df_wc = helper.wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            plt.imshow(df_wc)
            st.pyplot(fig)

            #most common words
            most_common_df = helper.most_common_words(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(most_common_df[0], most_common_df[1], color='violet')
            plt.xticks(rotation='vertical')

            st.title('most common words')
            st.pyplot(fig)

            st.dataframe(most_common_df)





