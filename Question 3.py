
#### Question 3:
import json
import pandas as pd
from datetime import datetime
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mypassword",
  database="unigap",
  auth_plugin='mysql_native_password'
)


cursor = mydb.cursor()

# Step 1: Create the employees table
create_table_query = """
CREATE TABLE IF NOT EXISTS employees (
    id INT PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INT,
    join_date DATE
)
"""
cursor.execute(create_table_query)
mydb.commit()

# Function to load JSON file
def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to transform data
def transform_data(data):
    transformed_data = []
    for record in data:
        try:
            transformed_record = (
                int(record['id']),
                record['name'],
                record['department'],
                int(record['salary']),
                datetime.strptime(record['join_date'], '%Y-%m-%d').date()
            )
            transformed_data.append(transformed_record)
        except (KeyError, ValueError, TypeError) as e:
            print(f"Error transforming record {record}: {e}")
            continue
    return transformed_data

# Function to load data into the database
def load_data_to_db(data, cursor, mydb):
    insert_query = """
    INSERT INTO employees (id, name, department, salary, join_date)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.executemany(insert_query, data)
        mydb.commit()
        print(f"Successfully loaded {cursor.rowcount} records into the employees table.")
    except mysql.connector.Error as e:
        print(f"Error loading data into database: {e}")
        mydb.rollback()

if __name__ == "__main__":
    # File path to the JSON file
    json_file_path = 'employees.json'
    
    # Extract the data from the JSON file
    raw_data = load_json_file(json_file_path)
    
    # Transform the data
    transformed_data = transform_data(raw_data)
    
    # Load the transformed data into the database
    load_data_to_db(transformed_data, cursor, mydb)
    
    # Close the cursor and connection
    cursor.close()
    mydb.close()
