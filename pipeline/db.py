from mysql import connector
from dotenv import load_dotenv
import os
from .utils import logger

#load the environment variables from .env file
load_dotenv()
class DatabaseConnection:
    def __init__(self):
        self.DB_HOST=os.getenv("DB_HOST")
        self.DB_USER=os.getenv("DB_USER")
        self.DB_PASSWORD=os.getenv("DB_PASSWORD")
        self.DB_NAME=os.getenv("DB_NAME")

        try:
            self.connection=connector.connect(
                host=self.DB_HOST,
                user=self.DB_USER,
                password=self.DB_PASSWORD,
                database=self.DB_NAME)
            logger.info("Database connection established successfully")
        except Exception as e:
            self.connection=None
            logger.error(f"Failed to connect to the database. Please check the credentials and database status.Error:{str(e)}")    
        
    def execute_query(self,query):            
        if self.connection is not None:
            try:
                cursor=self.connection.cursor()
                cursor.execute(query)
                rows=cursor.fetchall()
                return True, rows
            except Exception as e:
                logger.error(f"Failed to execute the query. Error:{str(e)}")
                return False, str(e)
        return False, "Failed to connect to database"
