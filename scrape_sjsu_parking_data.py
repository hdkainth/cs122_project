import sys
import os
import argparse
import json
from pprint import pprint
from datetime import datetime

from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus
import requests
from requests.packages import urllib3

parser = argparse.ArgumentParser()
parser.add_argument('out_loc')
args = parser.parse_args()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Scrape the HTML elements from the SJSU parking webpage
url = "https://sjsuparkingstatus.sjsu.edu/"
response = requests.get(url, verify=False)
html_content = response.text

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the names of all the parking garages
garage_names = [span.text.strip() for span in soup.find_all('h2', class_='garage__name')]
# Extract the percentage fullness of the parking garages
fullness_values = [int(span.text.strip().split()[0]) for span in soup.find_all('span', class_='garage__fullness')]
# Extract the current timestamp
timestamp = soup.find('p', class_='timestamp').text.strip()

# Turn the timestamp into a datetime object
timestamp = " ".join(timestamp.split(" ")[2:5])
datetime_object = datetime.strptime(timestamp, "%Y-%m-%d %I:%M:%S %p")


# Create a dictionary containing the timestamp and another dictionary for the garage fullness values
garage_occupancy = { 'timestamp' : datetime_object.strftime("%Y-%m-%d %H:%M:%S"), 'garages': {} }

# Insert the garage fullness values in the dictionary
for index in range(len(garage_names)):
    garage_occupancy['garages'][garage_names[index]] = fullness_values[index];

# Create the output file name
output_file = 'sjsu_garage_info_' + datetime_object.strftime("%Y_%m_%d_%H_%M_%S") + '.txt'
output_file = os.path.join(args.out_loc, output_file)

# If the file exists, do nothing, else create the file and insert the dictionary into the MongoDB cluster
if os.path.exists(output_file):
    print(f"File {output_file} already existing")
else:
    f = open(output_file, 'w')
    print(garage_occupancy, file=f)

    username = quote_plus('sjsu_parking_db')
    password = quote_plus('ksa9365jkmdghs74')

    uri = "mongodb+srv://" + username + ":" + password + "@cluster0.oflgbpa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a new client and connect to the server
    client = MongoClient(uri)
    sjsu_parking_db = client['sjsu_parking']
    garage_data = sjsu_parking_db['garage_data']
    
    garage_info = garage_occupancy
    garage_info.update(garage_info['garages'])
    del garage_info['garages']

    garage_data.insert_one(garage_info)
    print(f"Inserted data: {garage_info}")
    print(garage_data.count_documents({}))

