import re
import pandas as pd

def processing(data):
    try:
        # Identifying the data pattern
        pattern = r'\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\u202f[ap]m - '

        # Message extraction
        messages = re.split(pattern, data)[1:]
        # Date extraction
        dates = re.findall(pattern, data)

        # Moving messages and dates into a DataFrame
        df = pd.DataFrame({'user_message': messages, 'message_date': dates})

        print("DataFrame before processing:")
        print(df.head())  # Print the DataFrame before processing

        if df.empty:
            raise ValueError("No data found")

        df['message_date'] = df['message_date'].str.split(' - ', expand=True)[0]

        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p')

        df.rename(columns={'message_date': 'date'}, inplace=True)

        # Splitting the user and message
        users = []
        messages = []
        for msg in df['user_message']:
            entry = re.split('([\w\W]+?):\s', msg)
            if entry[1:]:
                users.append(entry[1])
                messages.append(entry[2])
            else:
                users.append('group_notification')
                messages.append(entry[0])

        df['user'] = users
        df['message'] = messages
        df.drop(columns=['user_message'], inplace=True)

        # Splitting year, month, day, hour, minute
        df['only_date'] = df['date'].dt.date
        df['year'] = df['date'].dt.year
        df['month_num'] = df['date'].dt.month
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['day_name'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        df['message_date'] = df['date'].astype(str)

        period = []
        for hour in df[['day_name', 'hour']]['hour']:
            if hour == 23:
                period.append(str(hour) + '-' + str('00'))
            elif hour == 0:
                period.append(str(hour) + '-' + str('01'))
            else:
                period.append(str(hour) + '-' + str(hour + 1))
        df['period'] = period



        print("DataFrame after processing:")
        print(df.head())  # Print the DataFrame after processing

        return df

    except Exception as e:
        print(f"Error processing data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if an error occurs
