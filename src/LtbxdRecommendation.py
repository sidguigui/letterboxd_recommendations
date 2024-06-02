import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split, cross_validate
from Pgconnection import ReturningDF  # Assuming this is a custom module for database connection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def LtbxdRecommendation():
    # Load data from the database
    movies_df = pd.DataFrame(ReturningDF('SELECT * FROM public.moviesdb'))
    ratings_df = pd.DataFrame(ReturningDF('SELECT * FROM public.ratings'))

    # Drop rows with NaNs in the ratings dataset
    ratings_df = ratings_df.dropna(subset=['User', 'Name', 'Rating'])

    # Drop rows with NaNs in crucial columns in the movies dataset
    movies_df = movies_df.dropna(subset=['Genres', 'Themes', 'Actors', 'Director'])

    # Load the data into a Surprise dataset
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings_df[['User', 'Name', 'Rating']], reader)

    # Split the data into train and test sets
    trainset, testset = train_test_split(data, test_size=0.25)

    # Train the SVD algorithm
    algo = SVD()
    algo.fit(trainset)

    # Evaluate the algorithm
    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

    # Split the columns by delimiter and expand into separate columns
    genre_cols = movies_df['Genres'].str.split(';', expand=True).add_prefix('Genre')
    theme_cols = movies_df['Themes'].str.split(';', expand=True).add_prefix('Theme')
    actor_cols = movies_df['Actors'].str.split(';', expand=True).add_prefix('Actor')

    movies_df = pd.concat([movies_df, genre_cols, theme_cols, actor_cols], axis=1)
    movies_df.drop(['Actors', 'Themes', 'Genres'], axis=1, inplace=True)

    # Combine relevant features into a single string for content-based filtering
    movies_df['content'] = movies_df.apply(lambda row: ' '.join([str(value) if value is not None else '' for value in row[['Genre0', 'Genre1', 'Genre2', 'Theme0', 'Theme1', 'Theme2', 'Actor0', 'Actor1', 'Actor2', 'Director']]]), axis=1)

    # Convert the content into a matrix of TF-IDF features
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['content'])

    # Calculate the cosine similarity matrix 
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    #Preparing for loops
    movie_names = movies_df['Name'].tolist()

    user_ids = ratings_df['User'].unique()
    top_n = 10  # Number of top recommendations
    
    all_recommendations = []
    
    # Getting the watched films
    watched = pd.DataFrame(ReturningDF('SELECT * FROM public.ratings'))
    
    # Weights
    cf_weight = 0.5
    cbf_weight = 0.5
    
    # Loop to get the recommendations for each user   
    for user_id in user_ids:
        
        # Get movies already watched by the user
        user_watched_movies = watched[watched['User'] == user_id]['Name'].tolist()
        
        # Get collaborative filtering predictions, filtering out already wacthed movies
        cf_predictions = [(movie_name, algo.predict(user_id, movie_name).est) for movie_name in movie_names if movie_name not in user_watched_movies]
        
        # Get the top N movies from collaborative filtering
        cf_predictions.sort(key=lambda x: x[1], reverse=True)
        cf_top_movies = [movie_name for movie_name, _ in cf_predictions[:top_n]]
        
        # Initialize list for content-based filtering recommendations
        cbf_top_movies = []
        
        for movie_name in cf_top_movies:
            # Get the index of the movie
            idx = movies_df.index[movies_df['Name'] == movie_name].tolist()[0]
            # Get the similarity scores of all movies with that movie
            sim_scores = list(enumerate(cosine_sim[idx]))
            # Sort the movies based on the similarity scores
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            # Get the top N similar movies
            cbf_top_movies.extend([movies_df.iloc[i[0]]['Name'] for i in sim_scores[1:top_n+1]])
        
        # Combine CF and CBF recommendations and assign weights
        cf_dict = {movie: cf_weight for movie in cf_top_movies}
        cbf_dict = {movie: cbf_weight for movie in cbf_top_movies}
        
        final_scores = {}
        
        for movie, weight in cf_dict.items():
            if movie in final_scores:
                final_scores[movie] += weight
            else:
                final_scores[movie] = weight
        
        for movie, weight in cbf_dict.items():
            if movie in final_scores:
                final_scores[movie] += weight
            else:
                final_scores[movie] = weight
        
        # Sort movies by final scores
        sorted_final_scores = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Filter out already rated movies
        final_recommendations = [movie for movie, score in sorted_final_scores if movie not in user_watched_movies]
        
        # Take the top N from the blended list
        final_recommendations = final_recommendations[:top_n]
        
        # Collect recommendations for the user
        recommendations_df = pd.DataFrame({'User': [user_id] * len(final_recommendations), 'Name': final_recommendations})
        all_recommendations.append(recommendations_df)

    # Concatenate all user recommendations into a single DataFrame
    recommendations_final = pd.concat(all_recommendations, ignore_index=True)
    
    return recommendations_final
