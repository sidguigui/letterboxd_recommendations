# Letterboxd Recommendation Project
Developed by Guilherme Monteiro as a personal study on recommendation methods, this project explores the integration of content-based and collaborative filtering techniques.

#### -- Project Status: [Active]

## Project Intro/Objective
In an era where content availability is vast and overwhelming, we are confronted with a new dilemma: how to navigate and choose from so many possibilities. Streaming services have implemented various engines to recommend the next movie or series to watch. However, the challenge remains: how do we aggregate and manage all this data effectively? Social media platforms like Letterboxd have emerged to help users track and explore each other's favorite films. Letterboxd specially, allows users to catalog and share their movie-watching experiences. However, it lacks a personalized recommendation system.

With this in mind, I envisioned creating a recommendation system to help decide what movies to watch next by getting the data from Letterboxd. Given the structured data from such a system, I also saw an opportunity to develop a visualization tool to provide detailed film-watching analytics. And by using the exported data from my friends Letterboxd accounts, it was possible to create the training data set to validate the recommendation system created.

As Collaborative Filtering (CF) prediction is commonly employed in data coming from rating systems base systems a common problem, specially when utilizing few users it is the data sparsity. Caused by the lack of diversity in the movies composing of the dataframes. Therefore, a way to work with this problem is to create a hybrid paring it with a Conten Based Filtering (CBF) prediction. 

Thus, this project aims to enhance Letterboxd functionalities by adding a recommendation system based on two main machine-learning methods: Content-based and Collaborative filtering. Additionally, it involves analyzing Letterboxed data to understand user preferences and movie trends. The recommendation system will provide personalized movie suggestions. PostgreSQL will manage the data efficiently, supporting the recommendation system, while a Power BI dashboard will complement Letterboxd for visualization.

### Methods Used
* Recommendation system
* Content-based Filtering
* Collaborative Filtering
* Connection with PostgreSQL
* Data Visualization with Power BI

### Technologies
* Python
* PostgreSQL
* Power BI

## Project Description
This project created a robust movie recommendation system for Letterboxed by utilizing a combination of content-based and collaborative filtering techniques. Here are the main aspects of the project:

1. **Data Sources**:
   - Movie metadata including genres, cast, director, and synopsis.
   - User profile data (ratings) to enhance personalized recommendations.

2. **Questions and Hypotheses**:
   - Can combining content-based and collaborative filtering provide better recommendations than using either method alone?
   - What trends can be identified in user ratings over time?

3. **Data Analysis/Visualization**:
   - Analyze user rating distributions and patterns.
   - Visualize movie trends and popular genres over time.
   - Explore correlations between different movie attributes and user preferences.

4. **Modelling Work**:
   - Develop and compare different recommendation algorithms.
   - Implement and test hybrid models combining content-based and collaborative filtering.
   - Evaluate model performance using metrics like RMSE, precision, and recall.

5. **Challenges**:
   - Ensuring data quality and handling missing values.
   - Balancing between overfitting and generalization in the recommendation models.
   - Efficiently managing and querying datasets in PostgreSQL.

## Technical Background
### Recommendation system
As mentioned, the recommendation system was developed using the combined methods of Collaborative Filtering and Content-Based Filtering.

### Collaborative Filtering

The Collaborative Filtering was developed by training the SVD (Singular Value Decomposition) and SVD++ algorithm and cross validating it with the measures RMSE(Root Mean Square Error) and MAE(Mean Absolute Error), both measures to calculate the precision of the 
decomposition.

The surprise package will get the item [user_id,movie_name,rating] matrix and rearrange it to get the R matrix, in which will have the following configuration.

- $R$ is a $m \times n$ matrix
- $m$ is the number of users in the matrix
- $n$ is the number of all the movies in the entire rating system

In which the item $r_{ui}$ represents the rating given by user $u$ to film $i$.

Then, using the regular SVD decomposition $R = U \Sigma V^T$, the recommender system will produce the following decomposition 

$$R = U \Sigma V^T$$

Reducing the dimensionality to  $k$ latent factors, instead of using the full SVD, we can approximate $R$ using a reduced number of singular values and corresponding vectors. This is done by keeping only the top $k$ singular values and their corresponding vectors. 

$$R \approx U_k \Sigma_k V^T_k$$

where:
   - $U_K$ is the $m \times k$ matrix containing the first $k$ columns of $U$.
   - $\Sigma_k$ is the first $k \times k$ diagonal matrix containing the top $k$ singular values.
   - $V_k$ is the $n \times k$ matrix containing the first $k$ columns of $V$.

 To transform the above approximation into the desired form $R \approx PQ^T $ the transfoamtion steps are as follows.

$$P = U_k \Sigma_k^{1/2}$$
$$Q = V_k \Sigma_k^{1/2}$$
where:
 - $\Sigma_k^{1/2}$ is the square root of $\Sigma_k$

Then, the approximation of the original matrix gets to the result. 
$$R \approx P Q^T$$

where: 
- $P$ is an $m \times k$ matrix representing user preferences (user latent feature matrix)
- $Q$ is an $n \times k$ matrix representing the film characteristics (item latent feature matrix)

Each row in $P$ represent a user and each row of $Q$ represents a film.


$$\hat{r}_{ui} = \mu + b_u +b_i + q_i^T P_U$$

where:

- $\mu$ is the global mean of all ratings
- $b_u$ is the bias of user
- $b_i$ is the bias of film 
- $p_u$ is the latent feature vector for user
- $q_i$ is the latent feature vector for film

The matrices $P$ and $Q$ are learned through an optimization process, often using stochastic gradient descent (SGD). The objective is to minimize the regularized squared error between the observed ratings $r_{ui}$ and the predicted ratings $\hat{r}_{ui}$:

$$\min_{P, Q, b_u, b_i} \sum_{(u, i) \in \mathcal{K}} \left( r_{ui} - (\mu + b_u + b_i + q_i^T p_u) \right)^2 + \lambda \left( \|p_u\|^2 + \|q_i\|^2 + b_u^2 + b_i^2 \right)$$


Then it was used the 5-fold cross-validation, as the dataset is split into 5 equal-sized folds. The model is trained and evaluated 5 times, each time using a different fold as the validation set and the remaining 4 folds as the training set. This process helps to reduce the variance of the evaluation metrics by averaging results over multiple folds.

Then the output will show the RMSE and MAE for each of the 5 folds and provide the mean and standard deviation for these metrics across all folds. This helps you understand the performance and variability of your model. Using cross_validate with RMSE and MAE in 5-fold cross-validation provides a robust evaluation of your recommender system. It helps in understanding the model’s accuracy and error distribution, leading to more reliable and generalized performance insights.

In addition to the standard SVD approach, the SVD++ algorithm is also employed for collaborative filtering. SVD++ extends the SVD model by incorporating implicit feedback, which can improve the accuracy of the recommendations. Implicit feedback refers to indirect indicators of user preference, such as viewing history, clicks, or purchase records, which are not explicitly provided as ratings but can still inform the model about user interests. In SVD++, the user latent feature vector $p_u$ is enhanced with an additional term that accounts for the sum of item feature vectors associated with items that the user has interacted with, but not necessarily rated. This term adjusts the latent user vector by considering the influence of all items the user has implicitly engaged with. The prediction formula for SVD++ is given by:

$$\hat{r}_{ui} = \mu + b_u + b_i + q_i^T \left( p_u + \frac{1}{|N(u)|} \sum_{j \in N(u)} y_j \right)$$

where:
-  $N(u)$ is the set of items that user $u$ has interacted with
- $y_j$ is the implicit feedback vector for item $j$

This enhancement allows SVD++ to better capture the subtleties of user preferences by considering both explicit ratings and implicit interactions, often resulting in more accurate and personalized recommendations. Although the SVD++ algorithm was provided with the same data, the project did not foresee extracting additional information from the users beyond the ratings.

### Content-Based Filtering

To create the Content-Based Filtering recommendation, each movie's genres, themes, and actors are concatenated into a single string for each movie, to create an unified representation of each movie that includes all relevant features.

The TF-IDF (Term Frequency-Inverse Document Frequency) vectorization is used to convert textual data into numerical vectors. The Term Frequency (TF) measures the frequency of a word in a document film. It's calculated as the number of times a term appears in a document divided by the total number of terms in the document. 

$$TF(t,d)= \frac{f_{t,d}}{n_d}$$
where:
- $𝑡$ is the term (word) for which we are calculating the frequency
- $𝑑$ is the document in which the term frequency is being calculated
- $f_{t,d}$ is the number of times the term t appears in document 
- $d$ is the total number of terms in document


Furthermore, the Inverse Document Frequency (IDF) measures how important a term is across all films. It's calculated as the logarithm of the total number of documents divided by the number of documents containing the term. 

$$IDF_{t, D} =\log \bigg({\frac{N}{1+\{d\in D:t \in d\}}}\bigg)$$

where:
- $t$ is the term for which we are calculating the IDF
- $𝐷$ is the set of all documents
- $𝑁$ is the total number of documents in the document $D$
- $\{d∈D:t∈d\}$ is the number of documents in the document $D$ that contain the term $𝑡$


Finally, the TF-IDF score for a term in a document is calculated by multiplying its TF by its IDF, the result is a numerical vector for each document (film) where each element represents the TF-IDF score of a term in the document.

$$TF-IDF(t,d,D)=TF(t,d)×IDF(t,D)$$

For each user, the system identifies the films they have rated, then looks for similar films based on the cosine similarity scores. The cosine similarity scores indicate how similar two films are based on their TF-IDF vector representations. The system selects the top similar films and recommends them to the user.The process is repeated for each user, providing personalized recommendations based on their movie ratings and the similarity of films.

The cosine similarity is calculated between every pair of movies' TF-IDF vectors. With a higher cosine similarity score indicates greater similarity between two movies. It ranges from -1 (completely dissimilar) to 1 (identical). This similarity metric is used to find movies that are most similar to each other, enabling personalized recommendations.

$$\text{cosine}(\mathbf{A}, \mathbf{B}) = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$

### Used Python libraries
The Surprise library is a Python scikit for building and analyzing recommender systems that deal with explicit rating data. The functions used were 'Reader' to define the format of the ratings data, 'SVD' is the singular value decomposition algorithm, 'train_test_split' to separate the test and train dataframes, and finally 'cross_validate' to get the cross validation of an algorithm.


For the development of this project the libraries used were Scikit-learn and Surprise. Scikit-Learn has built-in machine learning algorithms and models, called estimators. Each estimator can be fitted to some data using its fit method. The functions used in this project were 'TfidfVectorizer' to create the TF-IDF matrix and 'linear_kernel' to measure similarity between two items based on their content.

## Recommendation system algorithm
1. Get the 'Ratings' and the 'Movies' dataframe from the PostgreSQL. 
1. Feed the 'Ratings' dataframe into an Surprise data set.
1. Split the train and tests set - test_size = 0.25.  
1. Train the SVD algorithm.
1. Evaluate the algorithm by printing the 'RMSE' and 'MAE' scores.
1. Prepare the 'Movies' dataframe to be fed into TF-IDF matrix by combining features into a single colum 'content'.
1. Fit the TF-IDF matrix.
1. Compute the cosine similarity matrix by the TF-IDF matrix.
1. Define the weights for each method.
1. Generate the list of Collaborative Filtering predicitions for the selected 'User Id'.
1. Get the top 10 films in the 'CF' dataframe.
1. For each top CF recommendation, it finds similar movies using CBF.
1. CF and CBF recommendations are combined with respective weights.
1. Movies are sorted based on the combined scores, and already watched movies are filtered out.
1. Top recommendations are collected and combined for all users.

## Training and testing recommendation method
The comparative analysis between SVD and SVD++ reveals that SVD++ slightly outperforms SVD in terms of predictive accuracy, with lower mean RMSE (0.6975 vs. 0.7054) and MAE (0.5535 vs. 0.5599). However, SVD is faster, with a mean fit time of 0.01 seconds compared to SVD++'s 0.20 seconds. Thus, SVD was chosen to be used in this project. 

#### SVD results: 
<div style="margin: 0 auto; width: fit-content;">

|                 | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | Mean  | Std    |
|-----------------|--------|--------|--------|--------|--------|-------|--------|
| RMSE (testset)  | 0.7174 | 0.6368 | 0.7980 | 0.6619 | 0.7129 | 0.7054| 0.0555 |
| MAE (testset)   | 0.5692 | 0.5136 | 0.6248 | 0.5204 | 0.5716 | 0.5599| 0.0403 |
| Fit time        | 0.00   | 0.00   | 0.01   | 0.01   | 0.00   | 0.01  | 0.00   |
| Test time       | 0.00   | 0.00   | 0.00   | 0.00   | 0.00   | 0.00  | 0.00   |
</div>

#### SVD++ results:

<div style="margin: 0 auto; width: fit-content;">

|                 | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | Mean  | Std    |
|-----------------|--------|--------|--------|--------|--------|-------|--------|
| RMSE (testset)  | 0.6861 | 0.7070 | 0.7010 | 0.6987 | 0.6946 | 0.6975| 0.0070 |
| MAE (testset)   | 0.5401 | 0.5680 | 0.5678 | 0.5501 | 0.5417 | 0.5535| 0.0122 |
| Fit time        | 0.19   | 0.21   | 0.21   | 0.20   | 0.20   | 0.20  | 0.01   |
| Test time       | 0.01   | 0.01   | 0.01   | 0.01   | 0.01   | 0.01  | 0.00   |
</div>

## Needs of this project

- Data exploration and descriptive statistics
- Development of recommendation algorithms
- Integration with PostgreSQL for data management
- Creation of Power BI dashboards for visualization
- Performance evaluation and tuning of models
- Documentation and user guide preparation

## Getting Started

1. Clone this repo (for help see this [tutorial](https://help.github.com/articles/cloning-a-repository/)).
2. Create a folder in the root directory called 'data\raw' and load the .zip files from the Letterboxd users.
3. Data processing/transformation scripts are being kept in the 'src\main.py' file.
4. Power BI dashboards are available in the 'reports\letterboxd.pbix'.
5. Install the Python libraries listed in the requirements.txt file.
6. Create a Postgres server with the following SQL statement.

    ```sql
    CREATE TABLE ratings (
        User VARCHAR (255) ,
        Name VARCHAR (255),
        Date DATE,
        Rating FLOAT
    );

    CREATE TABLE moviesdb (
        Name VARCHAR (255),
        Year INT,
        Date DATE,
        Genre VARCHAR (550),
        Theme VARCHAR (550),
        Actors VARCHAR (550),
        Director VARCHAR (255)
    );

    CREATE TABLE recommendation (
        User VARCHAR (255),
        Name VARCHAR (255)
    );
    ```
7. Connect the BI file on the Postgres DB. 
8. Run the 'src\main.py' file.

## Next steps
- Adapt the recommendation system to get only results from specific genres and themes.
- Add more data sources to the recommendation system.
- Store the recommendations to further validate the system success with the users.
- Create a web application to interact with the recommendation system.

## Contact
* Feel free to contact me if you are interested in contributing or giving insights and feedbacks!
* [LinkedIn](https://www.linkedin.com/in/guilherme-bezerra-monteiro/)