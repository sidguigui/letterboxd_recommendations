import numpy as np
import requests
from bs4 import BeautifulSoup
from Pgconnection import AddRowToTable

def LetterboxdScraper(ltbxd_scp,ltbxd_pg):
    ltbxd_scp.rename(columns={'Letterboxd URI': 'Letterboxd_URI'}, inplace=True)
    # Assuming ltbxd_wtchd is your merged DataFrame
    for index, row in ltbxd_scp.iterrows():
        title = row['Name']
        
        # Check if the movie already exists in the PostgreSQL DataFrame
        if title in ltbxd_pg['Name'].values:
            print(f"Skipping scraping for {title}. Data already exists in PostgreSQL.")
            continue
        
        url = row['Letterboxd_URI']
        
        # Add user-agent headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        # Sending a GET request to the URL
        response = requests.get(url, headers=headers)
        
        # Checking if the request was successful (status code 200)
        if response.status_code == 200:
            # Parsing the HTML content of the response
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Now you can work with the parsed HTML content
            print(f"Title of webpage {index}: {soup.title.string}")
            
            # Find the span with class 'directorlist'
            director_span = soup.find('span', class_='directorlist')

            # Extract the director's name from the span
            director_name = director_span.text.strip()
            
            # Extract genres from the specific section
            genre_section = soup.find('div', id='tab-genres')
            if genre_section:
                genre_tags = genre_section.find_all('a', class_='text-slug')
                genres = [tag.text for tag in genre_tags if '/films/genre/' in tag['href']]
                genres = [tag.text for tag in genre_tags[:3]]
            else:
                genres = ["Genres not found"]
            
            # Extract themes from the specific section
            if genre_section:
                theme_tags = genre_section.find_all('a', class_='text-slug')
                themes = [tag.text for tag in theme_tags if '/films/theme/' in tag['href'] or '/films/mini-theme/' in tag['href']]
                themes = [tag.text for tag in theme_tags[:3]]
            else:
                themes = ["Themes not found"]
            
            # Extract actors from the specific section
            actor_section = soup.find('div', id='tab-cast')
            if actor_section:
                actor_tags = actor_section.find_all('a', class_='text-slug')
                actors = [tag.text for tag in actor_tags]
                actors = [tag.text for tag in actor_tags[:3]]
            else:
                actors = ["Actors not found"]
            # Update the DataFrame with the director, genres, and themes
            ltbxd_scp.at[index, 'Director'] = director_name
            ltbxd_scp.at[index, 'Genres'] = '; '.join(genres)
            ltbxd_scp.at[index, 'Themes'] = '; '.join(themes)
            ltbxd_scp.at[index, 'Actors'] = '; '.join(actors)
            
            # Pass row as a dictionary to AddRowToTable function
            movie_data = tuple(ltbxd_scp.iloc[index])

            # Convert numpy.int64 types to native Python int types
            movie_data = tuple(int(item) if isinstance(item, np.int64) else item for item in movie_data)

            # Call AddRowToTable function with the table name and movie data
            AddRowToTable(movie_data)
        else:
            print(f"Failed to fetch data from URL {url} with status code {response.status_code}")