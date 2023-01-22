import datetime as dt
from http.client import CONTINUE
from operator import truediv
from optparse import Values
import os
from re import X
from haversine import haversine
from DbConnector import DbConnector
from tabulate import tabulate
import pymongo
from pymongo import MongoClient, version




class ExampleProgram:

    def __init__(self):
        self.connection = DbConnector()
        #self.db_connection = self.connection.db_connection
        #self.cursor = self.connection.cursor
        self.allUsers = os.listdir("TDT4225/exc3/dataset/dataset/Data")
        self.usersWithLabels = "TDT4225/exc3/dataset/dataset/labeled_ids.txt"

    def removeAndInsert(self):
        self.connection.removeCollection("User")
        self.connection.removeCollection("Activity")
        self.connection.removeCollection("Trackpoint")
        self.connection.addCollection("User")
        self.connection.addCollection("Activity")
        self.connection.addCollection("Trackpoint")
        
        self.connection.addIndexes("Activity", "user_id")
        self.connection.addIndexes("Activity", "transportation_mode")
        self.connection.addIndexes("Activity", "start_date")
        self.connection.addIndexes("Trackpoint", "activity_id")
        self.connection.addIndexes("Trackpoint", [("location", pymongo.GEOSPHERE)])
        
        
    def insertUser(self):
        allUsersForInsert = []
        usersWithLabels = []
        userdict = {}
        
        with open(self.usersWithLabels) as f:
            for i in f:
                content = i
                content = content.replace("\n", "")
                if len(content) <= 0:
                    continue 
                usersWithLabels.append(content)

   
        for user in self.allUsers:
            
            if len(user) != 3:
                continue 

            userContainsLabels = user in usersWithLabels
                
            userObj = {
                '_id': user,
                'has_labels': userContainsLabels
            }
            allUsersForInsert.append(userObj)
        
        self.connection.insertInCollection("User", allUsersForInsert)
        
        for user in usersWithLabels: 
            userLabelFile = open("TDT4225/exc3/dataset/dataset/Data/" + user + "/labels.txt")
            next(userLabelFile)
            userTransDict   = {}
                        
            for line in userLabelFile:
                
                line = line.replace("\n", " ")
                line = line.replace("\t", " ")
                line = line.replace("/", "-")
                
                line = line.split(" ")
                startDate = dt.datetime.strptime(line[0] + " " + line[1], "%Y-%m-%d %H:%M:%S")
                endDate = dt.datetime.strptime(line[2] + " " + line[3], "%Y-%m-%d %H:%M:%S")
                userTransDict[startDate] = [endDate, line[4]]
                
            
            userdict[user] = userTransDict
        
        #activity insert
        count = 0
        for user in allUsersForInsert:
            print(user, count)
            count += 1
            ls = os.listdir("TDT4225/exc3/dataset/dataset/Data/" + user['_id'] + "/Trajectory")
            for file in ls:
                if len(file) <= 0:
                    print("continue ")
                    continue
                if file[0] == ".":
                    print("continue")                    
                    continue
                
                
                activityFile = open("TDT4225/exc3/dataset/dataset/Data/" + user['_id'] + "/Trajectory/" + file)
                counter = 0
                starttime = ""
                endtime = ""
                trackpoints = []
                transMode = ""
                with open("TDT4225/exc3/dataset/dataset/Data/" + user['_id'] + "/Trajectory/" + file) as f:
                    x = len(f.readlines())
                
                if x >= 2506:
                    #print("skipping cause 2500")
                    continue
                
                for line in activityFile:
                    counter  += 1
                    if len(line) <= 50:
                        continue
                     
                    
                    
                    line = line.replace("\n", "")
                    line = line.replace("\t", "")
                    line = line.split(",")
                    date = dt.datetime.strptime(line[5] + " " + line[6], "%Y-%m-%d %H:%M:%S")
                    #print(date)
                    trackpointObj = {
                        'location': {
                            'type': 'Point',
                            'coordinates': [float(line[1]), float(line[0])]
                        },
                        'time': date,
                    }
                    
                    trackpoints.append(trackpointObj)
                print("fffffffffffffffffff")
                print(trackpoints[0]['time'])
                print(trackpoints[-1]['time'])
                noChangestarttime = trackpoints[0]['time']
                noChangeendtime = trackpoints[-1]['time']
                if user['has_labels']:
                    #starttime = noChangestarttime.replace(" ", "")
                    #starttime = noChangestarttime.replace("-", "/")
                    #endtime = noChangeendtime.replace(" ", "")
                    #endtime = noChangeendtime.replace("-", "/")
                    print("wwwwwwwwwwwwwwww")
                    nestDic = userdict[user['_id']]
                    if noChangestarttime in nestDic:
                        if userdict[user['_id']][noChangestarttime][0] == noChangeendtime:                            
                            transMode = userdict[user['_id']][noChangestarttime][1]
                            print(transMode)
                    
                activityObj = {
                    '_user_id': user['_id'],
                    'transportation_mode': transMode,
                    'start_date': trackpoints[0]['time'],
                    'end_date': trackpoints[-1]['time'],
                }
                                                        
                resId = self.connection.insertOneInCollection("Activity", activityObj)    
                activity_id = resId
                
                for trackpoint in trackpoints:
                    trackpoint['_activity_id'] = activity_id
                
                self.connection.insertInCollection("Trackpoint", trackpoints)
            
    def getNumberOfUsers(self):
        return self.connection.getNumberOfDocuments("User")
    
    def getNumberOfActivities(self):
        return self.connection.getNumberOfDocuments("Activity")
    
    def getNumberOfTrackpoints(self):
        return self.connection.getNumberOfDocuments("Trackpoint")

        
        
        
    


def main():
    program = None
    try:
        program = ExampleProgram()
        #program.removeAndInsert()
        #program.insertUser()


        #print("Number of users: " + str(program.getNumberOfUsers()))
        #print("Number of activities: " + str(program.getNumberOfActivities()))
        #print("Number of trackpoints: " + str(program.getNumberOfTrackpoints()))
        
        #print("Task 2", program.connection.average_activities_per_user())
        #print("Task 3")
        #dispArr = program.connection.users_with_most_activities()
        #print("Task 4: users taken a taxi")
        #program.connection.unique_users_taken_taxi()
        #print("Task 5: ")
        #print("Task 5", program.connection.count_transportation_mode())
        # print("Task 6A")
        # program.connection.get_year_with_most_activities()
        #print("Task 6B")
        #program.connection.get_year_with_most_hours()
        #print("Task 7")
        #program.connection.distance_walked_for_user_in_year("112", 2008)
        #print("Task 10")
        #program.connection.users_with_activity_in_lat_long(39.916, 116.397)
        print("Task 11")
        with open('TDT4225/exc3/dataset/dataset/labeled_ids.txt') as f:
            for line in f:
                # print(lines)
                line = line[:3]
                program.connection.list_most_used_transportation_mode_for_user(line)
        
        
        
        #UNCOMMENT THE INDIVIDUAL LINES TO INSERT THE DATA
        #program.insert_userData("User")
        #program.insert_activityData("Activity")
        #program.insert_labels()
        #program.calcDist()



    except Exception as e:
        print(e)
        print("ERROR: Failed to use database:", e)
    finally:
        if program:
            program.connection.close_connection()


if __name__ == '__main__':
    main()
