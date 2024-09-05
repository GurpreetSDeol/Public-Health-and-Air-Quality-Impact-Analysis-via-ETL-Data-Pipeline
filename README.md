# Overview
The goal of this project is to analyse and monitor weather and air pollution data for major global cities using a time series approach. This pipeline extracts real-time data from public APIs, stores it in a PostgreSQL database, and performs exploratory and time series analysis. The project focuses on identifying correlations between weather conditions and pollution levels, as well as forecasting future pollution trends.

#Data Sources
OpenWeather API: Provides real-time weather and air pollution data.
API Ninjas: Used to gather population, latitude, and longitude data for city selection.

#Project Structure and Contents

__Data__: Contains the raw and processed data files in .csv and .json formats.

__Data Analysis__: Contains Jupyter notebooks for analysis and PowerBI reports for visualizations.

__Data_ETL__/

SQL_Files: SQL scripts for creating and managing the PostgreSQL database.

City_selection.py: Script to collect population, latitude, and longitude data for city selection.

Weather_and_Pollution_ETL.py: Script for automating the extraction, transformation, and loading of weather and pollution data.

Final_city_data: Processed data in .csv and .json formats.

__Test_Folder__: Contains test files and initial scripts used during the early stages of development.

__Dockerfile__: Defines the Docker container configuration for the ETL process.

__requirements.txt__: Lists the dependencies required for the project.

# Repository Contents

__Data_ETL__/
City_selection.py: Script that retrieves population, latitude, and longitude values for selecting major cities.

_Weather_and_Pollution_ETL.py_: Script that extracts weather and pollution data, processes it, and loads it into the PostgreSQL database.

# Future Work

Forecasting Models: Expand forecasting capabilities to predict pollution levels using time series data.
Additional Data Sources: Integrate more datasets, such as industrial activity or traffic, to improve the analysis of pollution factors.
