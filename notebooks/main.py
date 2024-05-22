# ADICIONAR: 
    # -CHAMAR FUNÇÕES
    # -TIRAR A PARTE QUE LÊ O CSV
    # -DELETAR IPYNB
    # -ENTRAR TODOS OS DFS EM SUAS FUNÇÕES
    # -AJEITAR FOR
    # -AO FECHAR O PROGRAMA O PG TEM QUE ESTAR LOTADO   

import os
import zipfile
import shutil
import pandas as pd
from LetterboxdScraper import LetterboxdScraper 
from Pgconnection import ReturningDF, EnteringTable, DeleteAllRecords

# Call the ReturningDF function
ltbxd_pg = ReturningDF('SELECT * FROM public.moviesdb')
# Check the result
if ltbxd_pg is not None:
    print("Data retrieved.")
else:
    print("Failed to retrieve data.") 
    
DeleteAllRecords('ratings')

def unzip_and_delete(directory):
    # Listar arquivos no diretório
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        # Verificar se é um arquivo e se tem extensão .zip
        if os.path.isfile(item_path) and item.endswith('.zip'):
            print(f'Encontrado arquivo zip: {item}')
            # Extrair o arquivo zip
            with zipfile.ZipFile(item_path, 'r') as zip_ref:
                extract_path = os.path.join(directory, os.path.splitext(item)[0])
                zip_ref.extractall(extract_path)
                print(f'Extraído para: {extract_path}')
                              
                # Load the CSV file
                csv_file_path_ratings = os.path.join(extract_path, 'ratings.csv')
                csv_file_path_watched = os.path.join(extract_path, 'watched.csv')

                ratings = pd.read_csv(csv_file_path_ratings)
                ltbxd_scp = pd.read_csv(csv_file_path_watched)
                #RODAR SCRAPER
                LetterboxdScraper(ltbxd_scp,ltbxd_pg)
                
                #ENTRAR DADOS DE RATING NO PG
                # Add a new column 'User' with the value 'gbmonteiro' for all rows
                # Call the ReturningDF function 
                            
                ratings['User'] = extract_path.split('-')[1]

                # Select onlamey the required columns: 'User', 'Date', 'Rating'
                ratings = ratings[['User','Name', 'Date', 'Rating']]
                
                
                # Insert the DataFrame into the 'public.ratings' table
                EnteringTable("ratings", ratings)
                
                # Remover a pasta extraída
                shutil.rmtree(extract_path)
                print(f'Pasta removida: {extract_path}')

# Uso do exemplo
starting_directory = r'data/raw/'
unzip_and_delete(starting_directory)

print('FUNCIONOU!')
    