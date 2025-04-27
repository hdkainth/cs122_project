import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
from urllib.parse import quote_plus

# connecting to mongodb
username = quote_plus('sjsu_parking_db')
password = quote_plus('ksa9365jkmdghs74')
uri = "mongodb+srv://" + username + ":" + password + "@cluster0.oflgbpa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
sjsu_parking_db = client['sjsu_parking']
garage_data = sjsu_parking_db['garage_data']

# loading the data
parking_data = list(garage_data.find())
parking_df = pd.DataFrame(parking_data)

# turning timestamp into datetime obj
parking_df['timestamp'] = pd.to_datetime(parking_df['timestamp']) 

# get columns of each garage
garage_column = [col for col in parking_df.columns 
                  if col not in ['_id', 'timestamp']]

# using pandas melt function to unpivot the df from wide to long format
melted_parking_df = parking_df.melt(id_vars=['timestamp'], 
                                    value_vars=garage_column,
                                    var_name='garage_name', 
                                    value_name='fullness_value')

# time series to show availabily of each garage over time (daily)
for garage_name in melted_parking_df['garage_name'].unique():
    garage_df = melted_parking_df[melted_parking_df['garage_name'] == garage_name]

    plt.figure(figsize=(10, 7))
    plt.plot(garage_df['timestamp'], garage_df['fullness_value'], color='darkblue')
    plt.title(f'Parking Availability per Day for: {garage_name}')
    plt.xlabel('Date')
    plt.ylabel('Fullness Percentage (%)')
    plt.show()

# time series to show availability of each garage for the day (hourly)
melted_parking_df['timestamp'] = pd.to_datetime(melted_parking_df['timestamp'])
melted_parking_df['hour'] = melted_parking_df['timestamp'].dt.hour
hourly_parking_avg = melted_parking_df.groupby(['garage_name', 'hour'])['fullness_value'].mean().reset_index()

for garage_name in hourly_parking_avg['garage_name'].unique():
    garage_df = hourly_parking_avg[hourly_parking_avg['garage_name'] == garage_name]
    
    plt.figure(figsize=(10, 7))
    plt.bar(garage_df['hour'], 
            garage_df['fullness_value'], 
            color='darkblue')
    plt.title(f'Parking Availability per Hour for: {garage_name}')
    plt.xlabel('Time of Day')
    plt.ylabel('Fullness Percentage (%)')
    time = [f"{h:02d}:00" for h in garage_df['hour']]  
    # only showing every 2 hrs to make x axis label more readable
    plt.xticks(garage_df['hour'][::2], time[::2]) 
    plt.grid(True, axis='y')  
    plt.show()

# bar chart for average fullness by garage
average_fullness = melted_parking_df.groupby('garage_name')['fullness_value'].mean().sort_values()

plt.figure(figsize=(10, 5))
plt.barh(average_fullness.index, average_fullness.values, color='darkblue')
plt.title('Average Parking Fullness by SJSU Garage')
plt.xlabel('Average Fullness Percentage (%)')
plt.show()
