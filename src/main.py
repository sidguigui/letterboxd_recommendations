import os
import zipfile
import shutil
import numpy as np
import pandas as pd
from LetterboxdScraper import LetterboxdScraper 
from Pgconnection import ReturningDF, EnteringTable, DeleteAllRecords
from LetterboxdRecommendation import LetterboxdRecommendation

# Getting the Movies DB PostgreSQL 
movies_db = ReturningDF('SELECT * FROM public.moviesdb')

# Deleting previous ratings
DeleteAllRecords('ratings')

#Function to get the data from the .zip files
def UnzipDelete(directory):
    # List files in the directory
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        # Verify if is a .zip file
        if os.path.isfile(item_path) and item.endswith('.zip'):
            print(f'Zip file found: {item}')
            # Extract .zip file
            with zipfile.ZipFile(item_path, 'r') as zip_ref:
                extract_path = os.path.join(directory, os.path.splitext(item)[0])
                zip_ref.extractall(extract_path)
                print(f'Extracted to: {extract_path}')
                              
                # Load the CSV file
                csv_file_path_ratings = os.path.join(extract_path, 'ratings.csv')
                csv_file_path_watched = os.path.join(extract_path, 'watched.csv')

                ratings = pd.read_csv(csv_file_path_ratings)
                ltbxd_scp = pd.read_csv(csv_file_path_watched)
                
                #Running webscraper
                LetterboxdScraper(ltbxd_scp,movies_db)
                
                user = extract_path.split('-')[1]
                
                #Creating the 'Notrated' df to include 
                #fake dates(1900-01-01) and NaN into the rating                 
                notrated = pd.DataFrame()
                notrated['Name'] = ltbxd_scp [['Name']]
                notrated['User'] = user
                notrated['Date'] =  np.nan
                notrated['Date'].fillna(pd.Timestamp('1900-01-01'), inplace=True)
                notrated['Rating'] = np.nan
                notrated = notrated[['User','Name', 'Date', 'Rating']]
                
                ratings['User'] = user
                
                # Select the required columns: 'User', 'Date', 'Rating'
                ratings = ratings[['User','Name', 'Date', 'Rating']]
                unique_rows = notrated[~notrated['Name'].isin(ratings['Name'])]
                
                # Append these unique rows to df1
                ratings = pd.concat([ratings, unique_rows], ignore_index=True)
                ratings.drop_duplicates(keep='first', inplace=True)
           
                # Insert the DataFrame into the 'public.ratings' table
                EnteringTable("ratings", ratings)
                
                # Delete the extracted directory
                shutil.rmtree(extract_path)
                print(f'Removed directory: {extract_path}')
                              
# File directory
starting_directory = r'data/raw/'

#Running the UnzipDelete function
UnzipDelete(starting_directory)

#Deeleting Recomendation table in the DB
DeleteAllRecords('recommendation')

#Running the recommendation algorith
recommendation = LetterboxdRecommendation()

#Entering recommendation into DB
EnteringTable("recommendation", recommendation)

print(recommendation)
print('FUNCIONOU!')