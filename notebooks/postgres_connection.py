import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
import os
import logging

# Set up logging
logging.basicConfig(level=logging.ERROR)

# Entering database
db_user = os.getenv("DB_USER")
db_host = os.getenv("DB_HOST")
db_pswd = os.getenv("DB_PASSWORD")

def execute_query(db_name, query):
    try:
        engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pswd}@localhost:{db_host}/{db_name}')
        with engine.connect() as connection:
            result = connection.execute(query)
        return result
    except Exception as e:
        print(f"An error occurred while executing the query: {e}")
        return None  # You can choose to return a default value or raise the exception again

def returningdf_query(db_name, query):
    try:
        engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pswd}@localhost:{db_host}/{db_name}')
        result = engine.execute(query)
        return pd.DataFrame(result, columns=result.keys())  # Specify column names
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None # Return an empty DataFrame or handle the error in another way


def entering_table(db_name, table_name, df_enter):
    try:
        # Database connection
        engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pswd}@localhost:{db_host}/{db_name}')
        
        # Reflect existing table structure
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=engine)

        # Check if columns exist and add them if necessary
        for column in df_enter.columns:
            if column not in table.columns:
                # Add the missing column to the table
                column_type = 'VARCHAR'  # Set the appropriate data type
                engine.execute(f'ALTER TABLE {table_name} ADD COLUMN {column} {column_type};')
                logging.info(f'Column "{column}" added to {table_name} table.')

        # Insert data into the table
        df_enter.to_sql(table_name, engine, index=False, if_exists='replace')
        
        logging.info(f'Data inserted into {table_name} table successfully.')
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None