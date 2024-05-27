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
    movies_df['content'] = movies_df.fillna('').apply(
        lambda row: ' '.join(row[['Genre0', 'Genre1', 'Genre2', 'Theme0', 'Theme1', 'Theme2', 'Actor0', 'Actor1', 'Actor2', 'Director']]), axis=1
    )

    # Convert the content into a matrix of TF-IDF features
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['content'])

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Get all movie names
    movie_names = movies_df['Name'].tolist()
    
    # Iterate over each user and get recommendations
    user_ids = ratings_df['User'].unique()
    top_n = 10  # Number of top recommendations

    all_recommendations = []

    for user_id in user_ids:
        # Get movies already rated by the user
        user_rated_movies = ratings_df[ratings_df['User'] == user_id]['Name'].tolist()
        
        # Get collaborative filtering predictions, filtering out already rated movies
        cf_predictions = [(movie_name, algo.predict(user_id, movie_name).est) for movie_name in movie_names if movie_name not in user_rated_movies]
        # Get the top N movies from collaborative filtering
        cf_predictions.sort(key=lambda x: x[1], reverse=True)
        cf_top_movies = [movie_name for movie_name, _ in cf_predictions[:top_n]]
        
        # Get the indices of the top N movies
        cf_indices = [movies_df.index[movies_df['Name'] == movie_name][0] for movie_name in cf_top_movies]

        # Get the similarity scores of the top N movies with all movies
        sim_scores = cosine_sim[cf_indices].mean(axis=0)
        
        # Combine the similarity scores
        movie_sim_scores = list(enumerate(sim_scores))
        movie_sim_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Get the top N recommendations, filtering out already rated movies
        hybrid_top_movies = [movies_df.iloc[i[0]] for i in movie_sim_scores if movies_df.iloc[i[0]]['Name'] not in user_rated_movies][:top_n]
        
        # Collect recommendations for the user
        recommendations_df = pd.DataFrame({'User_ID': [user_id] * len(hybrid_top_movies), 'Movie_Name': [movie['Name'] for movie in hybrid_top_movies]})
        all_recommendations.append(recommendations_df)

    # Concatenate all user recommendations into a single DataFrame
    recommendations_final = pd.concat(all_recommendations, ignore_index=True)
    
    return recommendations_final