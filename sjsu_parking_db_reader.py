import sys
from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus
from datetime import datetime

garage_data_collection = None

class ParkingDBReader:

    # define an init function
    def __init__(self):
        # Connect to the MongoDB Database
        self.garage_data_collection = None

        username = quote_plus('sjsu_parking_db')
        password = quote_plus('ksa9365jkmdghs74')

        uri = "mongodb+srv://" + username + ":" + password + "@cluster0.oflgbpa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        # Create a new client and connect to the server
        client = MongoClient(uri)

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
            sys.exit(0)

        sjsu_parking_db = client['sjsu_parking']
        self.garage_data_collection = sjsu_parking_db['garage_data']
        print(f"Opened collection with document count {self.garage_data_collection.count_documents({})}")

    # Query all of the information currently in the database
    def read_data_all(self):
        garage_data = list(self.garage_data_collection.find({}, {'_id': 0}))
        return garage_data

    # Query information in the database with timestamps from start_date to end_date
    def read_data_in_range(self, start_date, end_date):
        if start_date is None or end_date is None:
            return self.read_data_all()

        start_datetime = datetime(start_date.year, start_date.month, start_date.day).strftime("%Y-%m-%d %H:%M:%S")
        end_datetime   = datetime(end_date.year  , end_date.month  , end_date.day).strftime("%Y-%m-%d %H:%M:%S")

        garage_data_search_dic = {'timestamp': { '$gte': start_datetime, '$lte': end_datetime } }
        
        garage_data = list(self.garage_data_collection.find(garage_data_search_dic, {'_id': 0}))
        return garage_data