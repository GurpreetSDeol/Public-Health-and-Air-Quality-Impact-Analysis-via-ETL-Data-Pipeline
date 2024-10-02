# Overview
The goal of this project is to analyze and monitor the impact of weather and air pollution on public health for major global cities using a time series approach. The pipeline extracts real-time data from public APIs, stores it in a PostgreSQL database, and performs exploratory and time series analysis. The project focuses on identifying correlations between weather conditions, pollution levels, and health outcomes, with ongoing efforts to forecast future pollution and its health impacts.

# Observation so Far:

The analysis reveals that while Delhi and Shanghai exhibit nearly double the pollution levels of Singapore, their pollution levels relative to population size are comparable to those of Singapore, Barcelona, and Sydney. In contrast, cities like Tokyo, London, New York, Seoul, and Paris show significantly lower pollution levels despite their larger populations, indicating that urban infrastructure may effectively mitigate pollution in these areas.

Furthermore, analyzing deaths related to atmospheric diseases proves challenging due to national-level data collection, which complicates the ability to accurately determine correlations between air pollution and health outcomes. The data suggests that ischaemic heart disease is the leading cause of deaths related to atmospheric conditions, particularly in New York (69.6%) and Sydney (60.3%). In contrast, lower respiratory infections account for only 30.2% of deaths in Seoul and 36.8% in Singapore, whereas they represent just 4.4% of total deaths in New York and Shanghai.

# Data Sources

__OpenWeather API__: Provides real-time weather and air pollution data.

__API Ninjas__: Used to gather population, latitude, and longitude data for city selection.

__World Health Organisation__: Data containing health statistics for each city. 

# Project Structure and Contents

__Data__: Contains the raw and processed data files in .csv and .json formats.

__Analysis.ipynb__ Jupyter notebook for analysis and plots for visualizations.

__Data_ETL__/

City_selection.py: Script to collect population, latitude, and longitude data for city selection.

Weather_and_Pollution_ETL.py: Script for automating the extraction, transformation, and loading of weather and pollution data.

Final_city_data: Processed data in .csv and .json formats.

__Dockerfile__: Defines the Docker container configuration for the ETL process.

__requirements.txt__: Lists the dependencies required for the project.

__Pollution and Weather Power BI Report__: Power BI report containing dashboards.


# Future Work

Forecasting Models: Expand forecasting capabilities to predict pollution levels using time series data.
Additional Data Sources: Integrate more datasets, such as industrial activity or traffic, to improve the analysis of pollution factors.
