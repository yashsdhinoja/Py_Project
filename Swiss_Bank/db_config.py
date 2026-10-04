import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="ca32icp",
            database="Swiss_Bank"
        )

        if connection.is_connected():
            print("Successfully Connected !!!")

        return connection
    
    except Error as e:
        print(f"Database Connection Error: {e}")
        return None

get_connection()