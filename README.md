# Overview
The goal of this project is to analyze and monitor the impact of transportation, weather, and air pollution on public health for major global cities using a time series approach. The pipeline extracts real-time data from public APIs, stores it in a PostgreSQL database, and performs exploratory and time series analysis. The project focuses on identifying correlations between public transport usage, weather conditions, pollution levels, and health outcomes, with ongoing efforts to forecast future pollution and its health impacts.

# Observation so Far:

Despite outlier cities having a significantly lower population, they contribute disproportionately more PM2.5 and PM10 particles, particularly between 15:00 and 19:00, the busiest time for daily commutes. This suggests that cities with better pollution control measures, or lower emissions, may handle the influx of pollutants more effectively.

Further analysis incorporating country development data could reveal patterns in how urban infrastructure and emissions control policies affect pollution levels, leading to actionable insights on how these cities manage air quality.

# Data Sources

__OpenWeather API__: Provides real-time weather and air pollution data.

__API Ninjas__: Used to gather population, latitude, and longitude data for city selection.

# Project Structure and Contents

__Data__: Contains the raw and processed data files in .csv and .json formats.

__Analysis.ipynb__ Jupyter notebook for analysis and plots for visualizations.

__Data_ETL__/

City_selection.py: Script to collect population, latitude, and longitude data for city selection.

Weather_and_Pollution_ETL.py: Script for automating the extraction, transformation, and loading of weather and pollution data.

Final_city_data: Processed data in .csv and .json formats.

__Dockerfile__: Defines the Docker container configuration for the ETL process.

__requirements.txt__: Lists the dependencies required for the project.


# Future Work

Forecasting Models: Expand forecasting capabilities to predict pollution levels using time series data.
Additional Data Sources: Integrate more datasets, such as industrial activity or traffic, to improve the analysis of pollution factors.
