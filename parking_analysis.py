import sys
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
from urllib.parse import quote_plus
import sjsu_parking_db_reader as db

def get_parking_data():
    db_reader = db.ParkingDBReader()
    parking_data = db_reader.read_data_all()
    df = pd.DataFrame(parking_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def plot_weekly_availability(df, garage_column):
    plt.figure(figsize=(10, 4))
    plt.title('Parking Availability for the Week')
    plt.xlabel('Date')
    plt.ylabel('Fullness Percentage (%)')

    for garage in garage_column:
        plt.plot(df['timestamp'], df[garage], label=garage)

    plt.legend(title="Garages", loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.tight_layout()
    plt.show()

def plot_daily_availability(df, garage_column):
    df['hours'] = df['timestamp'].dt.hour
    grouped = df.groupby('hours').mean().reset_index()

    plt.figure(figsize=(10, 4))
    plt.title('Parking Availability for Today')
    plt.xlabel('Time of Day')
    plt.ylabel('Fullness Percentage (%)')

    offset = -0.4
    for garage in garage_column:
        plt.bar(grouped['hours'] + offset, grouped[garage], 0.2, label=garage)
        offset += 0.2

    time_labels = [f"{h:02d}:00" for h in grouped['hours']]
    plt.xticks(grouped['hours'][::2], time_labels[::2])
    plt.grid(True, axis='y')
    plt.legend(title="Garages", loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.tight_layout()
    plt.show()

def plot_monthly_average(df, garage_column):
    mean_state = df[garage_column].mean()
    plt.figure(figsize=(8, 4))
    colors = plt.cm.tab10.colors  

    bars = plt.barh(garage_column, mean_state, color=colors[:len(garage_column)])

    plt.title('Parking Availability for the Month')
    plt.xlabel('Average Fullness Percentage (%)')

    plt.legend(bars, garage_column, title="Garages")

    plt.tight_layout()
    plt.show()

def plot_all(df, garage_column):
    plot_daily_availability()
    plot_weekly_availability()
    plot_monthly_average()

def analyze_parking(view='weekly'):
    df = get_parking_data()
    garage_column = [col for col in df.columns if col not in ['_id', 'timestamp']]

    if view == 'daily':
        plot_daily_availability(df, garage_column)
    elif view == 'weekly':
        plot_weekly_availability(df, garage_column)
    elif view == 'monthly':
        plot_monthly_average(df, garage_column)
    else:
        plot_all(df, garage_column)
