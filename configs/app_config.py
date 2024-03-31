from mongoengine import connect
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
load_dotenv()


def create_database_connection(app):

    app.config["MONGO_URI"] = os.getenv("MONGO_URL")
    db = PyMongo(app).db
    try:
        # Attempt to establish the database connection
        connect(db="python_mongo", host=os.getenv("MONGO_URL"))

        print("Database connection successful")
        return db
    except Exception as e:
        # Handle any exceptions that occur during the connection process
        print("Failed to establish database connection:", e)


# Call the function to create the database connection
# create_database_connection()
