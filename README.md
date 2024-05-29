# Project Name
Developed by Guilherme Monteiro as a personal study on recommendation methods, this project explores the integration of content-based and collaborative filtering techniques.

#### -- Project Status: [Active]

## Project Intro/Objective
This project aims to enhance Letterboxed functionalities by adding a recommendation system based on two main machine-learning methods: Content-based and Collaborative filtering. Additionally, it involves analyzing Letterboxed data to understand user preferences and movie trends. The recommendation system will provide personalized movie suggestions. PostgreSQL will manage the data efficiently, supporting the recommendation system, while a Power BI dashboard will complement Letterboxed for visualization.

### Methods Used
* Recommendation system
* Content-based Filtering
* Collaborative Filtering
* Connection with PostgreSQL
* Data Visualization

### Technologies
* Python
* PostgreSQL
* Power BI

## Project Description
This project seeks to create a robust movie recommendation system for Letterboxed by utilizing a combination of content-based and collaborative filtering techniques. Here are the main aspects of the project:

1. **Data Sources**:
   - User ratings and reviews from Letterboxed.
   - Movie metadata including genres, cast, director, and synopsis.
   - User profile data to enhance personalized recommendations.

2. **Questions and Hypotheses**:
   - How do user preferences vary based on genre, director, or cast?
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
   - Efficiently managing and querying large datasets in PostgreSQL.

## Theoric background
### Recommendation system
As mentioned, the recommendation system was developed using the combined methods of Collaborative Filtering and Content-Based Filtering.

### Collaborative Filtering

The Collaborative Filtering was developed by training the SVD (Singular Value Decomposition) algorithm and cross validating it with the measures RMSE(Root Mean Square Error) and MAE(Mean Absolute Error), both measures to calculate the precision of the 
decomposition.

The surprise package will get the item [user_id,movie_name,rating] matrix and rearrange it to get the R matrix, in which will have the following configuration.

- $R$ is a $m \times n$ matrix
- $m$ is the number of users in the matrix
- $n$ is the number of all the movies in the entire rating system

In which the item $r_{ui}$ represents the rating given by user $u$ to film $i$.

Then, instead of using the regular SVD decomposition $R = U \Sigma V^T$, the recommender system will produce the following decomposition 

$R \approx P Q^T$

where: 
- $P$ is an $m \times k$ matrix representing user preferences (user latent feature matrix)
- $Q$ is an $n \times k$ matrix representing the film characteristics (item latent feature matrix)

Each row in $P$ represent a user and each row of $Q$ represents a film.


$\hat{r}_{ui} = \mu + b_u +b_i + q_i^T P_U$

where:

- $\mu$ is the global mean of all ratings
- $b_u$ is the bias of user
- $b_i$ is the bias of film 
- $p_u $ is the latent feature vector for user
- $q_i$ is the latent feature vector for film

The matrices $P$ and $Q$ are learned through an optimization process, often using stochastic gradient descent (SGD). The objective is to minimize the regularized squared error between the observed ratings $r_{ui}$ and the predicted ratings $\hat{r}_{ui}$:

$\min_{P, Q, b_u, b_i} \sum_{(u, i) \in \mathcal{K}} \left( r_{ui} - (\mu + b_u + b_i + q_i^T p_u) \right)^2 + \lambda \left( \|p_u\|^2 + \|q_i\|^2 + b_u^2 + b_i^2 \right)$


Then it was used the 5-fold cross-validation, as the dataset is split into 5 equal-sized folds. The model is trained and evaluated 5 times, each time using a different fold as the validation set and the remaining 4 folds as the training set. This process helps to reduce the variance of the evaluation metrics by averaging results over multiple folds.

Then the output will show the RMSE and MAE for each of the 5 folds and provide the mean and standard deviation for these metrics across all folds. This helps you understand the performance and variability of your model. Using cross_validate with RMSE and MAE in 5-fold cross-validation provides a robust evaluation of your recommender system. It helps in understanding the model’s accuracy and error distribution, leading to more reliable and generalized performance insights.

### Content-Based Filtering

CONTINUE 


## Training recommendation method

## Needs of this project

- Data exploration and descriptive statistics
- Development of recommendation algorithms
- Integration with PostgreSQL for data management
- Creation of Power BI dashboards for visualization
- Performance evaluation and tuning of models
- Documentation and user guide preparation

## Getting Started

1. Clone this repo (for help see this [tutorial](https://help.github.com/articles/cloning-a-repository/)).
2. Create a folder in the root directory called 'data\raw' and load the .zip files from the Letterboxed users.
3. Data processing/transformation scripts are being kept [src\]
4. Power BI dashboards are available [here](Repo folder containing visualization scripts/dashboards)
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

## Featured Notebooks/Analysis/Deliverables
* [Data Exploration and Analysis](link)
* [Model Development and Evaluation](link)
* [Power BI Dashboard](link)
* [Blog Post](link)

## Contributing DSWG Members

**Team Leads (Contacts): [Guilherme Monteiro](https://github.com/guilherme-monteiro) (@gmonteiro)**

## Contact
* If you haven't joined the SF Brigade Slack, [you can do that here](http://c4sf.me/slack).
* Our slack channel is `#datasci-projectname`
* Feel free to contact team leads with any questions or if you are interested in contributing!