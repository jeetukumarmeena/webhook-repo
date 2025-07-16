from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
    
    def init_app(self, app):
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        database_name = os.getenv('DATABASE_NAME', 'github_webhooks')
        collection_name = os.getenv('COLLECTION_NAME', 'events')
        
        try:
            self.client = MongoClient(mongodb_uri)
            self.db = self.client[database_name]
            self.collection = self.db[collection_name]
            
            # Test the connection
            self.client.admin.command('ping')
            print(f"Successfully connected to MongoDB: {database_name}")
            
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise e
    
    def insert_event(self, event_data):
        """Insert a single event into MongoDB"""
        try:
            result = self.collection.insert_one(event_data)
            print(f"Event inserted with ID: {result.inserted_id}")
            return result
        except Exception as e:
            print(f"Error inserting event: {e}")
            raise e
    
    def get_latest_events(self, limit=50):
        """Get the latest events from MongoDB"""
        try:
            cursor = self.collection.find().sort('timestamp', -1).limit(limit)
            events = list(cursor)
            print(f"Retrieved {len(events)} events from database")
            return events
        except Exception as e:
            print(f"Error retrieving events: {e}")
            raise e
    
    def get_event_count(self):
        """Get total count of events in database"""
        try:
            count = self.collection.count_documents({})
            return count
        except Exception as e:
            print(f"Error counting events: {e}")
            return 0

mongo = MongoDB()