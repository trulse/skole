from pymongo import MongoClient, version
import datetime as dt

class DbConnector:
    """
    Connects to the MongoDB server on the Ubuntu virtual machine.
    Connector needs HOST, USER and PASSWORD to connect.

    Example:
    HOST = "tdt4225-00.idi.ntnu.no" // Your server IP address/domain name
    USER = "testuser" // This is the user you created and added privileges for
    PASSWORD = "test123" // The password you set for said user
    """

    def __init__(self,
                 DATABASE='yep',
                 HOST="tdt4225-29.idi.ntnu.no",
                 USER="test",
                 PASSWORD="test123"):
        uri = "mongodb://%s:%s@%s/%s" % (USER, PASSWORD, HOST, DATABASE)
        # Connect to the databases
        try:
            self.client = MongoClient(uri)
            self.db = self.client[DATABASE]
        except Exception as e:
            print("ERROR: Failed to connect to db:", e)

        # get database information
        print("You are connected to the database:", self.db.name)
        print("-----------------------------------------------\n")

    def close_connection(self):
        # close the cursor
        # close the DB connection
        self.client.close()
        print("\n-----------------------------------------------")
        print("Connection to %s-db is closed" % self.db.name)
        
    def addCollection(self, collection_name):
        # create a collection
        self.db.create_collection(collection_name)
        print("Collection %s created" % collection_name)
        
    def removeCollection(self, collection_name):
        # remove a collection
        self.db.drop_collection(collection_name)
        print("Collection %s removed" % collection_name)
    
    def addIndexes(self, collection_name, index):
        # add indexes
        self.db[collection_name].create_index(index)
        print("Index %s added to collection %s" % (index, collection_name))


    def insertInCollection(self, collection_name, data):
        # insert data in collection
        self.db[collection_name].insert_many(data)
        #print("Data inserted in collection %s" % collection_name)
        
    def insertOneInCollection(self, collection_name, data):
        # insert data in collection
        res = self.db[collection_name].insert_one(data)
        return res.inserted_id
        #print("Data inserted in collection %s" % collection_name)
        
    def getNumberOfDocuments(self, collection_name):
        # get number of documents in collection
        return self.db[collection_name].count()
    
    
    
    #TASK 2
    def average_activities_per_user(self):
        # get number of documents in collection
        yep = self.db.Activity.aggregate([{"$group": {"_id": "$_user_id", "count": {"$sum": 1}}}, {"$group": {"_id": "null", "avg": {"$avg": "$count"}}}])
        return yep.next()['avg']
        
    #TASK 3
    def users_with_most_activities(self):
        # get number of documents in collection
        yep = self.db.Activity.aggregate([{"$group": {"_id": "$_user_id", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}, {"$limit": 20}])
        #dispArr = []
        for i in range (20):
            print(yep.next())
            # print("\n")
        #return dispArr
    
    
    #TASK 4
    def unique_users_taken_taxi(self):
        # get number of documents in collection
        yep = self.db.Activity.distinct("_user_id", {"transportation_mode": "taxi"})
        for i in range (len(yep)):
            print(yep[i])
    
    #TASK 5
    def count_transportation_mode(self):
        # get number of documents in collection
        yep = self.db.Activity.aggregate([{"$group": {"_id": "$transportation_mode", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}])
        print("Transportation mode count:")
        i = 0
        for i in range (11):
            if i == 0:
                i = i + 1
                yep.next()
                continue
            
            print(yep.next())
            
    
    #TASK 6A
    def get_year_with_most_activities(self):
        # get number of documents in collection
        yep = self.db.Activity.aggregate([{"$group": {"_id": {"$year": "$start_date"}, "count": {"$sum": 1}}}, {"$sort": {"count": -1}}, {"$limit": 1}])
        print("Year with most activities:")
        for i in range (1):
            print(yep.next())
    
    #TASK 6B
    def get_year_with_most_hours(self):
        # get number of documents in collection
        yep = self.db.Activity.aggregate([{"$group": {"_id": {"$year": "$start_date"}, "count": {"$sum": "$distance"}}}, {"$sort": {"count": -1}}, {"$limit": 1}])
        print("Year with most hours:")
        for i in range (1):
            print(yep.next()['_id'])
            
    
    #TASK 7
    def distance_walked_for_user_in_year(self, user_id, year):
        # get number of documents in collection
        yep = self.db.Activity.aggregate([{"$match": {"_user_id": user_id, "start_date": {"$gte": dt.datetime(year, 1, 1), "$lt": dt.datetime(year+1, 1, 1)}}}, {"$group": {"_id": "$_user_id", "count": {"$sum": "$distance"}}}])
        print("Distance walked for user %s in year %s:" % (user_id, year))
        for i in range (1):
            print(yep.next())
    
    #TASK 8
    
    #TASK 10
    def users_with_activity_in_lat_long(self, lat, lon):
        # get number of documents in collection
        yep = self.db.Activity.distinct("_user_id", {"start_location": {"$near": {"$geometry": {"type": "Point", "coordinates": [lon, lat]}}}})
        print("Users with activity in lat %s and long %s:" % (lat, lon))
        for i in range (yep.count()):
            print(yep.next())
    
    #TASK 11
    def list_most_used_transportation_mode_for_user(self, user_id):
        # get number of documents in collection
        yep = self.db.Activity.aggregate([{"$match": {"_user_id": user_id}}, {"$group": {"_id": "$transportation_mode", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}, {"$limit": 11}])
        print("Most used transportation mode for user %s:" % (user_id))
        for i in range (11):
            if i == 0:
                i = i + 1
                yep.next()
                continue
            try:
                print(yep.next())
            except:
                break