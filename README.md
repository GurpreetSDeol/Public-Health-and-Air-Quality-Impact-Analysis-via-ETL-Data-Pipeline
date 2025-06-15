# 🌍 Public Health and Air Quality Impact Analysis

This project explores the relationship between **air pollution**, **weather conditions**, and **public health outcomes** across cities. By integrating real-time data with historical insights and World Health Organization (WHO) statistics, the dashboard provides an interactive and data-driven view of environmental trends and their impact on human health.

🔗 **Live App**: [Public Health & Air Quality Dashboard](https://public-health-and-air-quality-dashboard.streamlit.app/)

---

## 🚀 Project Summary

The project follows a full data pipeline approach:

1. **Data Ingestion (ETL)**: A Dockerised Python script fetches real-time pollution and weather data from the OpenWeather API and stores it in a local PostgreSQL database.  
2. **Data Storage**: A structured PostgreSQL database stores and organises both real-time and static data (such as city metadata and WHO health indicators).  
3. **Data Visualisation**: Data is visualised in two formats:
   - A **Streamlit dashboard** for real-time and historical interactive analysis.
   - A **Power BI report** for additional exploratory insights.
4. **Final Outcome**: The Streamlit app acts as the final user-facing product, combining live and historical analysis in an intuitive UI.

---

## 📊 Streamlit Dashboard

The Streamlit dashboard is the core component of this project. It enables users to:

- View **real-time** pollution and weather data across selected cities using the OpenWeather API.
- Explore **historical data** visualisations based on previously collected and processed datasets.
- Analyse **WHO health data** (e.g. deaths per 100,000 due to ambient air pollution) by city.
- Select cities, timeframes, pollutants, and weather variables to customise the insights.
- Monitor trends, assess environmental risks, and make data-driven conclusions.

The dashboard is hosted publicly here:  
👉 [https://public-health-and-air-quality-dashboard.streamlit.app](https://public-health-and-air-quality-dashboard.streamlit.app)

---

## 🔁 Project Flow

```

                                                           
  OpenWeather API   --->   Docker ETL Script   --->   PostgreSQL DB   --->   Streamlit Dashboard                                                     
                                                                                   
                  
```

---

## 📁 Repository Structure

```
├── Docker/
│   ├── Data_ETL/                                     #Scripts used for selecting cities
│   ├── Dockerfile                                    # Docker setup for the ETL pipeline
│   └── Docker_ETL_Script.py                          # Python script to fetch data and store it in PostgreSQL
│
├── SQL files/
│   ├── Database_creation.sql                         # SQL scripts for schema creation
│   ├── Populate_Cities_table.sql                     # SQL script for populating the Cities Table
│   └── Update_Fact_Table.sql                         # SQL script to update fact table t
│
├── Power BI and Analysis/
│   ├── Analysis.ipynb                                # Initial Jupyter notebook exploratory data analysis         
│   └── Power BI Report.pbix                          # Inital Power BI dashboard file for local analysis 
│
├── Streamlit Dashboard/
│   ├── app.py                                        # Main Streamlit app UI and logic
│   ├── API_data.py                                   # Core class handling API interaction and data processing
│   └── Data/                                         # Supporting data files 
│
└── README.md                                         # Project overview and instructions
```

---

## 🧰 Technologies Used

- **Python** (ETL, Streamlit)
- **Docker** (containerised ETL pipeline)
- **PostgreSQL** (relational database)
- **Streamlit** (interactive dashboard)
- **Plotly** (visualisation)
- **Pandas** (data manipulation)
- **Power BI** (local dashboard)

---

## 📌 Future Improvements

- Automate ETL via cloud scheduling or a CI/CD pipeline.
- Integrate additional health or environmental datasets.

