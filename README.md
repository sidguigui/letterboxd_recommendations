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