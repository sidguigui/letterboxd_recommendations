# Imports
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.exc import SQLAlchemyError
import os
import logging
import psycopg2
from psycopg2 import sql
import numpy as np

# Set up logging
logging.basicConfig(level=logging.ERROR)

# Database connection parameters
db_user = os.getenv("DB_USER")
db_host = os.getenv("DB_HOST")
db_pswd = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

config = {
    'dbname': db_name,
    'user': db_user,
    'password': db_pswd,
    'host': db_host
}


print(config)


# Define database connection URL
db_url = f'postgresql+psycopg2://{db_user}:{db_pswd}@{db_host}/{db_name}'

# Create SQLAlchemy engine
engine = create_engine(db_url)

# Function to execute queries
def ExecuteQuery(query):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
        return result
    except SQLAlchemyError as e:
        logging.error(f"An error occurred while executing the query: {e}")
        return None

# Function to return DataFrame from query
def ReturningDF(query):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df
    except SQLAlchemyError as e:
        logging.error(f"An error occurred: {e}")
        return None

# Function to enter data into a table
def EnteringTable(table_name, df_enter):
    try:
        # Reflect existing table structure
        metadata = MetaData()
        metadata.reflect(bind=engine)
        table = Table(table_name, metadata, autoload_with=engine)

        # Check if columns exist and add them if necessary
        with engine.connect() as connection:
            for column in df_enter.columns:
                if column not in table.columns:
                    column_type = 'VARCHAR'  # Set the appropriate data type
                    connection.execute(text(f'ALTER TABLE {table_name} ADD COLUMN {column} {column_type};'))
                    logging.info(f'Column "{column}" added to {table_name} table.')

        # Insert data into the table
        df_enter.to_sql(table_name, engine, index=False, if_exists='append')
        
        logging.info(f'Data inserted into {table_name} table successfully.')
    
    except SQLAlchemyError as e:
        logging.error(f"An error occurred: {e}")
        return None

# Function to add a row to a table
def AddRowToTable(movie_data):
    # Convert numpy types to native Python types
    converted_data = tuple(int(item) if isinstance(item, np.integer) else item for item in movie_data)
    
    # Create a SQL query with the table name included
    query = """INSERT INTO public.moviesdb ("Date", "Name", "Year", "Letterboxd_URI", "Director", "Genres", "Themes", "Actors") 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Execute the INSERT statement
                cur.execute(query, converted_data)
                # Commit the transaction
                conn.commit()
                print("Movie inserted successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
