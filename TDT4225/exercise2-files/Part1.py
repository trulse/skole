from operator import truediv
import os
from DbConnector import DbConnector
from tabulate import tabulate


class ExampleProgram:

    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor
        self.allUsers = os.listdir("TDT4225/exercise2-files/dataset/Data")
        self.usersWithLabels = "TDT4225/exercise2-files/dataset/labeled_ids.txt"

    def create_table(self, table_name, query):

        # This adds table_name to the %s variable and executes the query
        self.cursor.execute(query % table_name)
        self.db_connection.commit()

    def insert_data(self, table_name):
        counter = 0


        for user in self.allUsers: 
            if len(user) != 3:
                continue 
            isInserted = False

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

    def insert_activity(self, table_name):
        print("hello")

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
        program.create_table(table_name="User", query=userQuery)
        program.create_table(table_name="Activity", query=activityQuery)
        program.create_table(table_name="TrackPoint",query=trackQuery)

        program.insert_data("User")


    except Exception as e:
        print("ERROR: Failed to use database:", e)
    finally:
        if program:
            program.connection.close_connection()


if __name__ == '__main__':
    main()
