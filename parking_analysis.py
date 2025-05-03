from datetime import datetime, timedelta
import sys
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
from urllib.parse import quote_plus
import sjsu_parking_db_reader as db

# retrieve parking data from db w/in specified time range
def get_parking_data(start_time=None, end_time=None):
    db_reader = db.ParkingDBReader()
    parking_data = db_reader.read_data_in_range(start_time, end_time)
    df = pd.DataFrame(parking_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# plot a bar graph showing garage fullness for the day
def plot_daily_availability(df, garage_column):
    # extract and group data
    df['hours'] = df['timestamp'].dt.hour
    grouped = df.groupby('hours').mean().reset_index()

    # plot figure
    plt.figure(figsize=(10, 4))
    plt.title('Parking Availability for Today')
    plt.xlabel('Time of Day')
    plt.ylabel('Fullness Percentage (%)')

    # adjust bar position
    offset = -0.4

    # create bar chart
    for garage in garage_column:
        plt.bar(grouped['hours'] + offset, grouped[garage], 0.2, label=garage)
        offset += 0.2

    # add labels and legend
    time_labels = [f"{h:02d}:00" for h in grouped['hours']]
    plt.xticks(grouped['hours'][::2], time_labels[::2])
    plt.grid(True, axis='y')
    plt.legend(title="Garages", loc='center left', bbox_to_anchor=(1.0, 0.5))

    # display plot
    plt.tight_layout()
    plt.show()

# plot a line graph showing garage fullness for the week
def plot_weekly_availability(df, garage_column):

    # plot figure
    plt.figure(figsize=(10, 4))
    plt.title('Parking Availability for the Week')
    plt.xlabel('Date')
    plt.ylabel('Fullness Percentage (%)')

    # create line graph
    for garage in garage_column:
        plt.plot(df['timestamp'], df[garage], label=garage)

    # display plot and legend
    plt.legend(title="Garages", loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.tight_layout()
    plt.show()

# plot a bar graph showing garage fullness for the month
def plot_monthly_average(df, garage_column):

    # calculate average fullness
    mean_state = df[garage_column].mean()

    # plot figure
    plt.figure(figsize=(8, 4))
    colors = plt.cm.tab10.colors  
    bars = plt.barh(garage_column, mean_state, color=colors[:len(garage_column)])

    # add labels and legend
    plt.title('Parking Availability for the Month')
    plt.xlabel('Average Fullness Percentage (%)')
    plt.legend(bars, garage_column, title="Garages")

    # display plot
    plt.tight_layout()
    plt.show()

# plots all graphs in a single popup
def plot_all(df, garage_column):
    # create figure with 3 subplots 
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 7))
    plt.subplots_adjust(hspace=0.8) 

    # plot daily fullness
    df['hours'] = df['timestamp'].dt.hour
    df_hours = df.groupby('hours').mean().reset_index()

    ax2.set_title('Parking Availability for Today', pad=20)  
    ax2.set_xlabel('Time of Day')
    ax2.set_ylabel('Fullness Percentage (%)')

    offset = -0.4

    for garage_name in garage_column:
        ax2.bar(df_hours['hours'] + offset, df_hours[garage_name], 0.2, label=garage_name)
        offset += 0.2

    # format time on x-axis to show every 2 hrs
    time = [f"{h:02d}:00" for h in df_hours['hours']]
    ax2.set_xticks(df_hours['hours'][::2])
    ax2.set_xticklabels(time[::2]) 
    ax2.grid(True, axis='y')

    ax2.legend(title="Garages", loc='upper left', bbox_to_anchor=(1, 1)) 

    # plot weekly fullness
    ax1.set_title('Parking Availability for the Week', pad=20)  
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Fullness Percentage (%)')

    for garage_name in garage_column:
        ax1.plot(df['timestamp'], df[garage_name], label=garage_name)

    ax1.legend(title="Garages", loc='upper left', bbox_to_anchor=(1, 1))  

    # plot monthly fulless
    mean_state = df[garage_column].mean()
    colors = plt.cm.tab10.colors  # Use a color map for distinct colors
    bars = ax3.barh(garage_column, mean_state, color=colors[:len(garage_column)])  

    ax3.set_title('Parking Availability for the Month', pad=20)  
    ax3.set_xlabel('Average Fullness Percentage (%)')

    ax3.legend(bars, garage_column, title="Garages", loc='upper left', bbox_to_anchor=(1, 1)) 

    # display all 3 plots
    plt.tight_layout(pad=3.0)  
    plt.show()


# analyze parking data and generate plot based on selection
def analyze_parking(view, start_time=None, end_time=None):
    # retrieve and load data
    df = get_parking_data(start_time, end_time)
    garage_column = [col for col in df.columns if col not in ['_id', 'timestamp']]

    # display plot based on view
    if view == 'daily':
        plot_daily_availability(df, garage_column)
    elif view == 'weekly':
        plot_weekly_availability(df, garage_column)
    elif view == 'monthly':
        plot_monthly_average(df, garage_column)
    elif view == 'all':
        plot_all(df, garage_column)
    #elif view == 'custom':
        # plot custom 
    else:
        plot_all(df, garage_column)