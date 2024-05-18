import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.exc import SQLAlchemyError
import os
import logging

# Set up logging
logging.basicConfig(level=logging.ERROR)

# Entering database
db_user = os.getenv("DB_USER")
db_host = os.getenv("DB_HOST")
db_pswd = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

def ExecuteQuerry(query):
    try:
        engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pswd}@{db_host}/{db_name}')
        with engine.connect() as connection:
            result = connection.execute(text(query))
        return result
    except SQLAlchemyError as e:
        logging.error(f"An error occurred while executing the query: {e}")
        return None

def ReturningDF(query):
    try:
        engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pswd}@{db_host}/{db_name}')
        with engine.connect() as connection:
            result = connection.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df
    except SQLAlchemyError as e:
        logging.error(f"An error occurred: {e}")
        return None

def EnteringTable(table_name, df_enter):
    try:
        # Database connection
        engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pswd}@{db_host}/{db_name}')
        
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
    
    
def AddRowToTable(table_name, df_row):
    try:
        engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pswd}@{db_host}/{db_name}')
        with engine.connect() as connection:
            # Convert the pandas row to a dictionary
            row_dict = df_row.to_dict()
            
            # Generate the columns and values for the INSERT statement
            columns = ', '.join(row_dict.keys())
            values = ', '.join([f":{key}" for key in row_dict.keys()])
            
            # Prepare the SQL statement
            sql = text(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
            
            # Execute the SQL statement
            connection.execute(sql, **row_dict)
        
        logging.info(f'Row added to {table_name} table successfully.')
    except SQLAlchemyError as e:
        logging.error(f"An error occurred: {e}")
        return None