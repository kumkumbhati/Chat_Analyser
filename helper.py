import pandas as pd
from collections import Counter
from urlextract import URLExtract
from wordcloud import WordCloud
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

extract = URLExtract()

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    # For col 1
    num_messages = df.shape[0]

    # For col 2
    words = []
    for message in df['message']:
        words.extend(message.split())

    # For col 3
    num_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]

    # For col 4
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_msg, len(links)


def most_busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df


def wordcloud(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    text = ' '.join(df['message'])
    df_wc = wc.generate(text)
    return df_wc

def most_common_words(selected_user, df):
    # Read stop words from file
    with open('stop_hinglish.txt', 'r') as f:
        stop_words_hinglish = f.read().splitlines()

    stop_words = set(stopwords.words('english')) | set(stop_words_hinglish)

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def monthly_timline(selected_user, df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].rest_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))



def monthly_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + '-' + timeline['year'].astype(str)

    return timeline

def daily_timeline(selected_user, df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    u_heatmap = df.pivot_table(index='day', columns='period', values='message', aggfunc='count').fillna(0)
    return u_heatmap
