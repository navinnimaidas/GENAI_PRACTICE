from mysql import connector
from dotenv import load_dotenv
import os

#load the environment variables from .env file
load_dotenv()
DB_HOST=os.getenv("DB_HOST")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_NAME=os.getenv("DB_NAME")

#create the connection to the database
class DatabaseConnection:
    def get_connection(self):
        try:
            connection=connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME)
            return True, connection
        except Exception as e:
            return False, str(e)
        
    def execute_query(self, connection,query):            
        try:
            cursor=connection.cursor()
            cursor.execute(query)
            rows=cursor.fetchall()
            return True, rows
        except Exception as e:
            return False, str(e)
        return False, "Failed to connect to database"
