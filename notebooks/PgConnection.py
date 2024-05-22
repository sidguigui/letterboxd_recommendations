import pandas as pd
import psycopg2
import psycopg2.extras as extras
from psycopg2 import sql
import logging
import numpy as np
import os

# Set up logging
logging.basicConfig(level=logging.ERROR)

# Direct database connection parameters
config = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST")
}

# Function to return DataFrame from query
def ReturningDF(query: str) -> pd.DataFrame:
    try:
        with psycopg2.connect(**config) as conn:
            df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return pd.DataFrame()

# Function to enter data into a table
def EnteringTable(table_name: str, df_enter: pd.DataFrame) -> None:
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Check if columns exist and add them if necessary
                cur.execute(sql.SQL("SELECT column_name FROM information_schema.columns WHERE table_name = %s"), [table_name])
                existing_columns = [row[0] for row in cur.fetchall()]

                for column in df_enter.columns:
                    if column not in existing_columns:
                        column_type = 'VARCHAR'  # Adjust this to handle different data types dynamically if needed
                        cur.execute(sql.SQL("ALTER TABLE {} ADD COLUMN {} {}").format(
                            sql.Identifier(table_name),
                            sql.Identifier(column),
                            sql.SQL(column_type)
                        ))
                        logging.info(f'Column "{column}" added to {table_name} table.')

                # Insert data into the table
                tuples = [tuple(x) for x in df_enter.to_numpy()]
                cols = sql.SQL(', ').join(map(sql.Identifier, df_enter.columns))
                query = sql.SQL("INSERT INTO {} ({}) VALUES %s").format(
                    sql.Identifier(table_name),
                    cols
                )
                extras.execute_values(cur, query, tuples)
                conn.commit()
                logging.info(f'Data inserted into {table_name} table successfully.')
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Function to add a row to a table
def AddRowToTable(movie_data: tuple) -> None:
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
                logging.info("Movie inserted successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error: {error}")
        

def DeleteAllRecords(table_name):
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(sql.SQL("DELETE FROM public.{}").format(sql.Identifier(table_name)))
        # Commit the transaction
        config.commit()
        
        print("All records deleted successfully.")

    
