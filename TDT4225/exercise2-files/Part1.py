from datetime import datetime, date
from http.client import CONTINUE
from operator import truediv
from optparse import Values
import os
from haversine import haversine
from DbConnector import DbConnector
from tabulate import tabulate


class ExampleProgram:

    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor
        self.allUsers = os.listdir("TDT4225/exercise2-files/dataset/dataset/Data")
        self.usersWithLabels = "TDT4225/exercise2-files/dataset/dataset/labeled_ids.txt"

    def create_table(self, table_name, query):

        # This adds table_name to the %s variable and executes the query
        self.cursor.execute(query % table_name)
        self.db_connection.commit()

    def insert_userData(self, table_name):
        counter = 0
        for user in self.allUsers: 
            isInserted = False
            if len(user) != 3:
                continue 

            with open(self.usersWithLabels) as f:
                for i in f:
                    content = f.readline()
                    if len(content) <= 0:
                        continue 

                    if int(content) == counter:
                        query = "INSERT IGNORE INTO %s (id,has_labels) VALUES ('%s',True)"
                        self.cursor.execute(query % (table_name, user))
                        isInserted = True
                        break
            
            if isInserted:
                counter+=1
                continue

            query = "INSERT IGNORE INTO %s (id,has_labels) VALUES ('%s',False)"
            self.cursor.execute(query % (table_name, user))
            counter+=1
        self.db_connection.commit()

    def insert_activityData(self, table_name):
        counter = 1
        maxCounter = 1
        for user in self.allUsers: 
            if len(user) != 3:
                continue 

            print("adding activities and track for user: "+user)

            onUser = os.listdir("TDT4225/exercise2-files/dataset/dataset/Data/"+user+"/Trajectory")

            for activity in onUser:
                with open(r"TDT4225/exercise2-files/dataset/dataset/Data/"+user+"/Trajectory/"+activity, 'r') as fp:
                    x = len(fp.readlines())
                    if x >= 2506:
                        print("skipped")
                        continue
                with open(r"TDT4225/exercise2-files/dataset/dataset/Data/"+user+"/Trajectory/"+activity, 'r') as fp:
                    counterTrack = 0
                    rows = []
                    print(counter)
                    for line in fp:
                        if len(line) <= 0 or counterTrack <= 5:
                            counterTrack+=1
                            continue
                        line = line.split(",")
                        if len(line) <= 0:
                            continue
                        if counterTrack == 6:
                            starttime = line[5]+" "+line[6]
                        if counterTrack == x-1:
                            endtime = line[5]+" "+line[6]
                        rows.append((maxCounter, counter, line[0], line[1],line[3], line[5]+" "+line[6][:8]))
                        maxCounter+=1
                        counterTrack+=1
                    values = ', '.join(map(str, rows))
                    print(counter)
                    query = "INSERT IGNORE INTO %s (id, user_id, transportation_mode, start_date_time, end_date_time) VALUES ('%s','%s', null, '%s', '%s')"
                    self.cursor.execute(query % (table_name, counter, user, starttime, endtime))
                    self.db_connection.commit()
                    sql = "INSERT INTO TrackPoint (id, activity_id, lat, lon, altitude, data) VALUES {}".format(values)
                    self.cursor.execute(sql)

                counter+=1
            self.db_connection.commit()

    def insert_labels(self):
        with open(self.usersWithLabels) as f:
            for i in f:
                with open(r"TDT4225/exercise2-files/dataset/dataset/Data/"+str(i[:3])+"/labels.txt", 'r') as fp:
                    counter = 0
                    for line in fp:
                        line = line.replace("/", "-")
                        line = line.replace("\t", " ")
                        line = line.replace("\n", " ")

                        line = line.split(" ")
                        if len(line) <= 0 or counter <= 0:
                            counter+=1
                            continue
                        query = """UPDATE Activity SET transportation_mode = '%s' WHERE start_date_time IN('%s') AND end_date_time IN('%s') AND user_id IN('%s');"""
                        self.cursor.execute(query % (line[4], line[0]+" "+line[1], line[2]+" "+line[3], i[:3]))
            self.db_connection.commit()

    def calcDist(self):
        coordQuery = """Select
                lat,
                lon
            from
                TrackPoint
            where
                activity_id in (
                SELECT id from Activity WHERE user_id = 112 and transportation_mode = 'walk' and YEAR(start_date_time)='2008' and year(end_date_time)='2008' 
            )"""
        self.cursor.execute(coordQuery)
        allCoordinates = self.cursor.fetchall()
        cumulativeDistance = 0
        print("Calculating distance...")
        for i in range(len(allCoordinates)):
            if i == len(allCoordinates)-1:
                break
            tempDistance = haversine(allCoordinates[i], allCoordinates[i+1], unit='km')
            cumulativeDistance += tempDistance
            print("Distance: "+str(cumulativeDistance))
        print("-----------------------------")
        print("TOTAL DISTANCE WALKED FOR USER 112: "+str(cumulativeDistance) + " km")


    def fetch_data(self, table_name):
        query = "SELECT * FROM %s"
        self.cursor.execute(query % table_name)
        rows = self.cursor.fetchall()
        print("Data from table %s, raw format:" % table_name)
        print(rows)
        # Using tabulate to show the table in a nice way
        print("Data from table %s, tabulated:" % table_name)
        print(tabulate(rows, headers=self.cursor.column_names))
        return rows

    def drop_table(self, table_name):
        print("Dropping table %s..." % table_name)
        query = "DROP TABLE %s"
        self.cursor.execute(query % table_name)

    def show_tables(self):
        self.cursor.execute("SHOW TABLES")
        rows = self.cursor.fetchall()
        print(tabulate(rows, headers=self.cursor.column_names))


def main():
    program = None
    try:
        program = ExampleProgram()
        userQuery = """CREATE TABLE IF NOT EXISTS %s (
            id VARCHAR(10) NOT NULL PRIMARY KEY,
            has_labels BOOLEAN)
        """
        activityQuery = """CREATE TABLE IF NOT EXISTS %s (
                   id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                   user_id VARCHAR(10) NOT NULL,
                   transportation_mode VARCHAR(30),
                   start_date_time DATETIME,
                   end_date_time DATETIME,
                   FOREIGN KEY (user_id) 
                        REFERENCES User(id) 
                        ON DELETE CASCADE
                   )
                """

        trackQuery = """CREATE TABLE IF NOT EXISTS %s (
                   id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                   activity_id INT NOT NULL,
                   lat DOUBLE,
                   lon DOUBLE,
                   altitude INT,
                   data DATETIME,
                   FOREIGN KEY (activity_id) 
                        REFERENCES Activity(id)
                        ON DELETE CASCADE
                   )
                """

        #UNCOMMENT THE INDIVIDUAL LINES TO CREATE THE TABLES        
        #program.create_table(table_name="User", query=userQuery)
        #program.create_table(table_name="Activity", query=activityQuery)
        #program.create_table(table_name="TrackPoint",query=trackQuery)

        #UNCOMMENT THE INDIVIDUAL LINES TO INSERT THE DATA
        #program.insert_userData("User")
        #program.insert_activityData("Activity")
        #program.insert_labels()
        program.calcDist()



    except Exception as e:
        print(e)
        print("ERROR: Failed to use database:", e)
    finally:
        if program:
            program.connection.close_connection()


if __name__ == '__main__':
    main()
