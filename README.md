# Overview
The goal of this project is to analyse and monitor weather and air pollution data for major global cities using a time series approach. This pipeline extracts real-time data from public APIs, stores it in a PostgreSQL database, and performs exploratory and time series analysis. The project focuses on identifying correlations between weather conditions, pollution levels and population, as well as forecasting future pollution trends.

# Observation:

Despite the outlier countries having almost half the population of other cities, they contribute significantly more PM2.5 and PM10 particles. The difference in pollution levels is almost double between 15:00 and 19:00, which is usually the busiest part of the day due to commutes from school or work.

This disparity could indicate that some cities have better pollution management systems in place, which reduces atmospheric pollutants, or that other cities produce far more emissions. Given the difference in population between the two groups, I believe the former is more likely. This highlights how effective infrastructure and pollution control measures can significantly reduce emissions. To verify this, I could use country development data in cojuction to discover any patterns. 


# Data Sources

__OpenWeather API__: Provides real-time weather and air pollution data.

__API Ninjas__: Used to gather population, latitude, and longitude data for city selection.

# Project Structure and Contents

__Data__: Contains the raw and processed data files in .csv and .json formats.

__Analysis.ipynb__ Jupyter notebook for analysis and plots for visualizations.

__Data_ETL__/

SQL_Files: SQL scripts for creating and managing the PostgreSQL database.

City_selection.py: Script to collect population, latitude, and longitude data for city selection.

Weather_and_Pollution_ETL.py: Script for automating the extraction, transformation, and loading of weather and pollution data.

Final_city_data: Processed data in .csv and .json formats.

__Test_Folder__: Contains test files and initial scripts used during the early stages of development.

__Dockerfile__: Defines the Docker container configuration for the ETL process.

__requirements.txt__: Lists the dependencies required for the project.


# Future Work

Forecasting Models: Expand forecasting capabilities to predict pollution levels using time series data.
Additional Data Sources: Integrate more datasets, such as industrial activity or traffic, to improve the analysis of pollution factors.
