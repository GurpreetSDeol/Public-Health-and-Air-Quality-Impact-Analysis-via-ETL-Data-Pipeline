import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc
import streamlit as st
from API_data import WeatherPollutionFetcher  
import json 

# Title for the dashboard
st.title(" Air Quality and Public Health Dashboard")
st.markdown("""

Explore how air pollution, weather conditions, and health outcomes vary across cities using both real-time and historical data.

This interactive dashboard enables you to:
- Analyse historical data or fetch live data via the OpenWeather API.
- Compare pollution and weather indicators across multiple cities.
- Visualise air quality trends and assess their health impacts.
- Examine World Health Organization (WHO) data on deaths attributed to ambient air pollution (per 100,000 population).


[ View the GitHub Repository](https://github.com/GurpreetSDeol/Public-Health-and-Air-Quality-Impact-Analysis-via-ETL-Data-Pipeline)  
[ Portfolio Website](https://gurpreetsdeol.github.io/)
""")



# Load Cities Data (Used in both modes)
cities_df = pd.read_csv('Streamlit Dashboard/Data/Cities.csv')
cities_df['marker_size'] = (cities_df['population'] / cities_df['population'].max()) * 50

# Define color palette
city_colors = pc.qualitative.Plotly

# Function to return a consistent city-color map
def get_city_color_map(cities_df):
    unique_cities = cities_df['city_name'].unique()
    return {city: color for city, color in zip(unique_cities, city_colors)}

city_color_map = get_city_color_map(cities_df)

#City Section

st.subheader(" Key Population Insights")
st.write("This section provides an overview of the cities, their population sizes, and geographical locations. The map below visualizes the cities based on population, and you'll also find key population metrics for the most populated cities.")


# Normalize Population for Marker Size
max_population = cities_df['population'].max()
cities_df['marker_size'] = (cities_df['population'] / max_population) * 50

# Create the Map Figure
fig = go.Figure()

fig.add_trace(go.Scattermapbox(
    lat=cities_df['latitude'],
    lon=cities_df['longitude'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=cities_df['marker_size'],
        color=cities_df['population'],
        colorscale='Viridis',
        showscale=True,
        sizemode='diameter'
    ),
    text=cities_df['city_name'] + '<br>Population: ' + cities_df['population'].astype(str),
    hoverinfo='text'
))

# Set Layout: World View
fig.update_layout(
    mapbox=dict(
        style="open-street-map",
        center=dict(lat=cities_df['latitude'].mean(), lon=cities_df['longitude'].mean()),  
        zoom=1.5,  
    ),
    margin={"r":0,"t":0,"l":0,"b":0},
    height=700
)


#Key info Cards

# Find the Highest Population City
max_pop_row = cities_df.loc[cities_df['population'].idxmax()]
highest_city_name = max_pop_row['city_name']
highest_city_population = max_pop_row['population']
national_population = max_pop_row['national_population']
country_name = max_pop_row['country']

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label=" Most Populated City", 
        value=highest_city_name, 
        delta=f"Population: {highest_city_population:,}"
    )

with col2:
    st.metric(
        label=" National Population", 
        value=country_name, 
        delta=f"Population: {national_population:,}"
    )

st.divider()

st.subheader(" 2D Map: Cities by Population Size")
st.write("Each city is represented based on its geographic location. Marker size and color intensity reflect population.")
st.plotly_chart(fig)

st.divider()

# Mode Selector
mode = st.sidebar.radio(
    "Select Mode",
    ["Historical data", "Live data"]
)

# Initialize session state variables only if not already set
if "weather_df" not in st.session_state:
    st.session_state.weather_df = pd.DataFrame()

if "pollution_df" not in st.session_state:
    st.session_state.pollution_df = pd.DataFrame()



#Sidebar settings

# Data Selection Section
city_options = cities_df['city_name'].unique().tolist()
selected_cities = st.sidebar.multiselect(
    label="Select Cities", 
    options=city_options, 
    default=city_options
)

# Pollutant options with display names
pollutant_options = {
    "PM₂.₅": "pm2_5",
    "PM₁₀": "pm10",
    "NO₂": "no2",
    "O₃": "o3",
    "CO": "co",
    "SO₂": "so2",
    "NH₃": "nh3"
}


selected_pollutant_label = st.sidebar.selectbox(
    label="Select Pollutant Type",
    options=list(pollutant_options.keys()),
    index=0
)
selected_pollutant = pollutant_options[selected_pollutant_label]

# Weather options with display names
weather_options = {
    "Temperature": "temperature",
    "Feels Like": "feels_like",
    "Humidity": "humidity",
    "Visibility": "visibility",
    "Wind Speed": "wind_speed",
    "Cloud Cover": "clouds_all"
}
selected_weather_label = st.sidebar.selectbox(
    label="Select Weather Parameter",
    options=list(weather_options.keys()),
    index=0
)
selected_weather_param = weather_options[selected_weather_label]


weather_units = {
    "temperature": "°C",
    "humidity": "%",
    "wind_speed": "m/s",
    "feels_like": "°C",
    "visibility": "m",
    "clouds_all": "%"

}

selected_unit = weather_units.get(selected_weather_param, "")




if mode == "Historical data":

  
    st.subheader(" Historical Data")
    st.write("This mode uses historical data for pollution, weather, and health analysis. Note that the insights may be limited due to inconsistencies in the available data.")


    pollution_df = pd.read_csv('Streamlit Dashboard/Data/Pollution.csv')
    weather_df = pd.read_csv('Streamlit Dashboard/Data/Weather.csv')
    who_df = pd.read_csv('Streamlit Dashboard/Data/Who Data.csv')

    pollution_df['date_time'] = pd.to_datetime(pollution_df['date_time']).dt.floor('H')
    weather_df['date_time'] = pd.to_datetime(weather_df['date_time']).dt.floor('H')

    pollution_df['local_time'] = pd.to_datetime(pollution_df['local_time']).dt.floor('H')
    weather_df['local_time'] = pd.to_datetime(weather_df['local_time']).dt.floor('H')

    #  Merge df with city df 
    pollution_df = pollution_df.merge(cities_df[['city_id', 'city_name']], on='city_id')
    weather_df = weather_df.merge(cities_df[['city_id', 'city_name']], on='city_id')


    #Sidebar settings
    # Date Range Selector
    
    available_dates = sorted(pollution_df['local_time'].dt.date.unique())

    selected_dates = st.sidebar.multiselect(
        label="Select Available Dates",
        options=available_dates,
        default=available_dates  # Default to all dates with data
    )


    # Pollution Section


    st.subheader(" Pollution Insights")
    st.write("This section visualizes the pollution levels of various pollutants such as PM₂.₅, PM₁₀, NO₂, O₃, CO, SO₂, and NH₃ across selected cities. You can explore how pollutant levels change over time and their relationship with city population.")


    # Filter based on cities
    filtered_pollution_df = pollution_df[pollution_df['city_name'].isin(selected_cities)]

    # Filter based on selected cities and dates
    filtered_pollution_df = pollution_df[
        (pollution_df['city_name'].isin(selected_cities)) &
        (pollution_df['local_time'].dt.date.isin(selected_dates))
    ]

    # Prepare Data for First Plot: Average pollutant over 24 hours
    filtered_pollution_df['hour_of_day'] = filtered_pollution_df['local_time'].dt.hour
    avg_pollutant_by_city_hour = filtered_pollution_df.groupby(
        ['city_name', 'hour_of_day']
    )[selected_pollutant].mean().reset_index()


    #  Plot the first graph: Avg pollutant by city over 24 hours
    fig_avg_24h_city = px.line(
        avg_pollutant_by_city_hour,
        x='hour_of_day',
        y=selected_pollutant,
        color='city_name', 
        markers=True,
        color_discrete_map=city_color_map,
        labels={
            'hour_of_day': 'Hour of Day',
            selected_pollutant: f'Avg {selected_pollutant.upper()}',
            'city_name': 'City'
        },
        title=f"Average {selected_pollutant_label} Levels Throughout the Day (by City)"
    )

    fig_avg_24h_city.update_layout(
        xaxis=dict(tickmode='linear', tick0=0, dtick=1),
        yaxis_title=f"{selected_pollutant_label} Concentration (µg/m³)",
        xaxis_title="Hour of Day (Local Time)"
    )

    # Prepare Data for Second Plot: Average pollutant per city + Population
    avg_pollutant_by_city = filtered_pollution_df.groupby('city_name')[selected_pollutant].mean().reset_index()
    avg_pollutant_by_city = avg_pollutant_by_city.merge(
        cities_df[['city_name', 'population']], 
        on='city_name', 
        how='left'
    )

    # Create the figure with two bars: one for pollutant levels and one for population

    fig_bar_comparison = go.Figure(
        data=[
            # Pollutant bar
            go.Bar(
                name=f"Avg {selected_pollutant.upper()} (µg/m³)",
                x=avg_pollutant_by_city['city_name'],
                y=avg_pollutant_by_city[selected_pollutant],
                yaxis='y',  
                offsetgroup=1,
                marker_color='blue'
            ),
            # Population bar 
            go.Bar(
                name="Population",
                x=avg_pollutant_by_city['city_name'],
                y=avg_pollutant_by_city['population'],
                yaxis='y2',  
                offsetgroup=2,
                marker_color='orange'
            )
        ],
        layout={
            'title': f"Comparison of Average {selected_pollutant_label} Levels and Population Across Cities",
            'yaxis': {'title': f'Avg {selected_pollutant_label} (µg/m³)'},
            'yaxis2': {
                'title': 'Population',
                'overlaying': 'y',  
                'side': 'right'     
            },
            'barmode': 'group',  
            'xaxis': {'title': 'City', 'tickangle': -45},
            'height': 600,
            'legend': {'x': 0.5, 'y': 1.05, 'orientation': 'h', 'xanchor': 'center'}
        }
    )

    # Pollution Cards

    # 1. City with the Highest Average Pollution (based on selected pollutant)
    avg_pollutant_by_city = filtered_pollution_df.groupby('city_name')[selected_pollutant].mean().reset_index()
    max_avg_pollution_city = avg_pollutant_by_city.loc[avg_pollutant_by_city[selected_pollutant].idxmax()]
    max_avg_pollution_city_name = max_avg_pollution_city['city_name']
    max_avg_pollution_value = max_avg_pollution_city[selected_pollutant]

    # 2. City with the Highest Pollution at any given time
    max_pollution_city = filtered_pollution_df.loc[filtered_pollution_df[selected_pollutant].idxmax()]
    max_pollution_city_name = max_pollution_city['city_name']
    max_pollution_value = max_pollution_city[selected_pollutant]

    # 3. Hour with the Highest Pollution Value
    max_pollution_hour = filtered_pollution_df.loc[filtered_pollution_df[selected_pollutant].idxmax()]
    max_pollution_hour_value = max_pollution_hour[selected_pollutant]
    max_pollution_hour_time = max_pollution_hour['local_time'].strftime('%H:%M')

    # Cards: City with Highest Average Pollution, City with Highest Pollution, Hour with Highest Pollution
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label=f" City with Highest Average {selected_pollutant.upper()} Pollution", 
            value=max_avg_pollution_city_name,
            delta=f"{max_avg_pollution_value:.2f} µg/m³"
        )

    with col2:
        st.metric(
            label=f" City with Highest {selected_pollutant.upper()} Pollution", 
            value=max_pollution_city_name,
            delta=f"{max_pollution_value:.2f} µg/m³"
        )

    with col3:
        st.metric(
            label=f" Hour with Highest {selected_pollutant.upper()} Pollution", 
            value=max_pollution_hour_time,
            delta=f"{max_pollution_hour_value:.2f} µg/m³"
        )

    # Display the First and Second Pollution Plots
    st.plotly_chart(fig_avg_24h_city)
    st.plotly_chart(fig_bar_comparison)



    # --- Weather Section


    st.subheader(" Weather Insights")
    st.write("This section focuses on weather parameters like temperature, humidity, and wind speed. It provides insights into how weather conditions vary across cities over the course of a day.")


    # Filter based on cities for weather
    filtered_weather_df = weather_df[weather_df['city_name'].isin(selected_cities)]

    # Prepare Data for First Plot: Average weather parameter over 24 hours
    filtered_weather_df['hour_of_day'] = filtered_weather_df['local_time'].dt.hour
    avg_weather_by_city_hour = filtered_weather_df.groupby(
        ['city_name', 'hour_of_day']
    )[selected_weather_param].mean().reset_index()

    # Plot the first graph: Avg weather parameter by city over 24 hours
    fig_avg_24h_weather = px.line(
        avg_weather_by_city_hour,
        x='hour_of_day',
        y=selected_weather_param,
        color='city_name',  
        markers=True,
        color_discrete_map=city_color_map,
        labels={
            'hour_of_day': 'Hour of Day',
            selected_weather_param: f'Avg {selected_weather_param.capitalize()}',
            'city_name': 'City'
        },
        title=f"Average {selected_weather_label} Throughout the Day (by City)"
    )

    fig_avg_24h_weather.update_layout(
        xaxis=dict(tickmode='linear', tick0=0, dtick=1),
        yaxis_title=f"{selected_weather_label} ({selected_unit})",
        xaxis_title="Hour of Day (Local Time)"
    )

    # Prepare Data for Second Plot: Average weather parameter per city
    avg_weather_by_city = filtered_weather_df.groupby('city_name')[selected_weather_param].mean().reset_index()

    # --- Plot the second graph: Avg weather parameter by city
    fig_bar_weather_comparison = px.bar(
        avg_weather_by_city,
        x='city_name',
        y=selected_weather_param,
        color='city_name',  
        color_discrete_map=city_color_map,
        labels={
            'city_name': 'City',
            selected_weather_param: f"Avg {selected_weather_param.capitalize()}"
        },
        title=f"Comparison of Average {selected_weather_label} Across Cities"
    )

    fig_bar_weather_comparison.update_layout(
        yaxis_title=f"Avg {selected_weather_label} ({selected_unit})",
        xaxis_title="City",
        xaxis_tickangle=-45,  
        barmode='group',
        showlegend=False
    )

    # Weather Cards

    # 1. City with the Highest Temperature
    max_temp_city = weather_df.loc[weather_df['temperature'].idxmax()]
    max_temp_city_name = max_temp_city['city_name']
    max_temp_value = max_temp_city['temperature']

    # 2. City with the Lowest Temperature
    min_temp_city = weather_df.loc[weather_df['temperature'].idxmin()]
    min_temp_city_name = min_temp_city['city_name']
    min_temp_value = min_temp_city['temperature']

    # 3. City with the Highest Humidity
    max_humidity_city = weather_df.loc[weather_df['humidity'].idxmax()]
    max_humidity_city_name = max_humidity_city['city_name']
    max_humidity_value = max_humidity_city['humidity']

    # Cards: City with Highest Temperature, City with Lowest Temperature, City with Highest Humidity
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label=" City with Highest Temperature", 
            value=f"{max_temp_city_name}",
            delta=f"{max_temp_value}°C"
        )

    with col2:
        st.metric(
            label=" City with Lowest Temperature", 
            value=f"{min_temp_city_name}",
            delta=f"{min_temp_value}°C"
        )

    with col3:
        st.metric(
            label=" City with Highest Humidity", 
            value=f"{max_humidity_city_name}",
            delta=f"{max_humidity_value}%"
        )

    st.divider()


    # Display the First and Second Weather Plots
    st.plotly_chart(fig_avg_24h_weather)
    st.plotly_chart(fig_bar_weather_comparison)



    # WHO data section

    # Sidebar for selecting multiple causes of death
    cause_options = who_df['cause'].unique().tolist()
    selected_causes = st.sidebar.multiselect(
        label="Select Causes of Death", 
        options=cause_options, 
        default=cause_options  # Default to all causes
    )


    st.subheader(" WHO Data Insights")
    st.write("This section incorporates data from the World Health Organization (WHO) about deaths caused by ambient air pollution. You can analyse the impact of pollution on health outcomes across cities, including the number of deaths per 100,000 people.")

    # Merge WHO data with the population data from cities_df
    who_data_with_population = who_df.merge(cities_df[['city_id', 'population']], on='city_id')

    # Filter WHO data for selected cities and selected causes
    who_filtered_df = who_data_with_population[
        (who_data_with_population['city_name'].isin(selected_cities)) &
        (who_data_with_population['cause'].isin(selected_causes))
    ]

    # Calculate deaths per 100,000 people
    who_filtered_df['deaths_per_100k'] = (who_filtered_df['deaths'] / who_filtered_df['population']) * 100000

    # Group by city and cause, and sum the deaths per 100k
    deaths_by_city_cause_100k = who_filtered_df.groupby(['city_name', 'cause'])['deaths_per_100k'].sum().reset_index()

    # Create the multilayer bar chart for deaths per 100,000 people
    fig_deaths_by_cause_100k = px.bar(
        deaths_by_city_cause_100k,
        x='city_name',
        y='deaths_per_100k',
        color='cause',
        barmode='stack',  # Stack the bars by cause
        labels={'deaths_per_100k': 'Deaths per 100,000 People', 'city_name': 'City', 'cause': 'Cause of Death'},
        title=f"Deaths per 100,000 People for Selected Causes by City"
    )

    fig_deaths_by_cause_100k.update_layout(
        xaxis_title="City",
        yaxis_title="Deaths per 100,000 People",
        xaxis_tickangle=-45,
        barmode='stack',
        showlegend=True,
        height=600
    )


    # WHO Data Cards for Total Deaths

    # Filter WHO data for Total Deaths
    total_deaths_df = who_df[who_df['cause'] == 'Total']

    # 1. City with the Highest Total Deaths
    max_total_deaths_city = total_deaths_df.loc[total_deaths_df['deaths'].idxmax()]
    max_total_deaths_city_name = max_total_deaths_city['city_name']
    max_total_deaths = max_total_deaths_city['deaths']

    # 2. City with the Lowest Total Deaths
    min_total_deaths_city = total_deaths_df.loc[total_deaths_df['deaths'].idxmin()]
    min_total_deaths_city_name = min_total_deaths_city['city_name']
    min_total_deaths = min_total_deaths_city['deaths']

    # Cards: City with Highest and Lowest Total Deaths
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label=" City with Highest Total Deaths", 
            value=f"{max_total_deaths_city_name}",
            delta=f"{max_total_deaths} deaths"
        )

    with col2:
        st.metric(
            label=" City with Lowest Total Deaths", 
            value=f"{min_total_deaths_city_name}",
            delta=f"{min_total_deaths} deaths"
        )

    st.divider()


    # Display the chart
    st.plotly_chart(fig_deaths_by_cause_100k)



elif mode == "Live data":

    st.subheader("Live Data")
    st.write("Click 'Fetch most recent data' to retrieve real-time weather and pollution data for the selected cities.")

    # Load data containing cities for the API
    OW_api_key = st.secrets['OW_api_key']
    json_save_path = rf'Streamlit Dashboard/Data/Final_city_data.json'
    with open(json_save_path) as f:
        city_data = json.load(f)

    fetcher = WeatherPollutionFetcher(OW_api_key, city_data)

    if st.sidebar.button("Fetch most recent data"):
        with st.spinner("Fetching data..."):
            fetcher.fetch_data()
            st.session_state.weather_df = fetcher.process_weather_data()
            st.session_state.pollution_df = fetcher.process_pollution_data()
            st.success("Data fetched successfully!")

    # Get latest data from session state
    weather_df = st.session_state.weather_df
    pollution_df = st.session_state.pollution_df

    # Only display if there's data
    if not pollution_df.empty and not weather_df.empty:
        # Merge with cities_df
        pollution_df = pollution_df.merge(cities_df[["city_id", "city_name"]], on="city_id", how="left")
        weather_df = weather_df.merge(cities_df[["city_id", "city_name"]], on="city_id", how="left")

        # Display
        st.subheader("Pollution Data")
        st.dataframe(pollution_df.head())

        st.subheader("Weather Data")
        st.dataframe(weather_df.head())

                
        st.subheader(" Pollution Insights")
        st.write("This section visualizes the pollution levels of various pollutants such as PM₂.₅, PM₁₀, NO₂, O₃, CO, SO₂, and NH₃ across selected cities.")
    
    
        #Pollution cards
    
        # 1. City with the Highest Average Pollution (based on selected pollutant)
        avg_pollutant_by_city = pollution_df.groupby('city_name')[selected_pollutant].mean().reset_index()
        max_avg_pollution_city = avg_pollutant_by_city.loc[avg_pollutant_by_city[selected_pollutant].idxmax()]
        max_avg_pollution_city_name = max_avg_pollution_city['city_name']
        max_avg_pollution_value = max_avg_pollution_city[selected_pollutant]
    
        # 2. City with the Lowest Average Pollution (based on selected pollutant)
        min_avg_pollution_city = avg_pollutant_by_city.loc[avg_pollutant_by_city[selected_pollutant].idxmin()]
        min_avg_pollution_city_name = min_avg_pollution_city['city_name']
        min_avg_pollution_value = min_avg_pollution_city[selected_pollutant]
    
    
        # Cards: City with Highest Average Pollution and City with Lowest Average Pollution
        col1, col2 = st.columns(2)
    
        with col1:
            st.metric(
                label=f" City with Highest Average {selected_pollutant.upper()} Pollution", 
                value=max_avg_pollution_city_name,
                delta=f"{max_avg_pollution_value:.2f} µg/m³"
            )
    
        with col2:
            st.metric(
                label=f" City with Lowest Average {selected_pollutant.upper()} Pollution", 
                value=min_avg_pollution_city_name,
                delta=f"{min_avg_pollution_value:.2f} µg/m³"
            )
    
    
        # Plot: Pollutant levels by city
        if not pollution_df.empty:
            pollution = pollution_df.groupby("city_name")[selected_pollutant].mean().reset_index()
           
            fig_pollution = px.bar(
                pollution,
                x="city_name",
                y=selected_pollutant,
                color="city_name",
                color_discrete_map=city_color_map,
                labels={"city_name": "City", selected_pollutant.upper(): "Pollutant Level"},
                title=f"Current {selected_pollutant_label} Levels by City"
            )
            fig_pollution.update_layout(showlegend=False, xaxis_title="City",
            yaxis_title=f"{selected_pollutant_label} Concentration (µg/m³)")
    
            st.plotly_chart(fig_pollution, use_container_width=True)
    
    
        #Weather cards
    
        st.subheader(" Weather Insights")
        st.write("This section focuses on weather parameters like temperature, humidity, and wind speed.")
    
    
        # 1. City with the Highest Temperature
        max_temp_city = weather_df.loc[weather_df['temperature'].idxmax()]
        max_temp_city_name = max_temp_city['city_name']
        max_temp_value = max_temp_city['temperature']
    
        # 2. City with the Lowest Temperature
        min_temp_city = weather_df.loc[weather_df['temperature'].idxmin()]
        min_temp_city_name = min_temp_city['city_name']
        min_temp_value = min_temp_city['temperature']
    
        # 3. City with the Highest Humidity
        max_humidity_city = weather_df.loc[weather_df['humidity'].idxmax()]
        max_humidity_city_name = max_humidity_city['city_name']
        max_humidity_value = max_humidity_city['humidity']
    
        # Cards: City with Highest Temperature, City with Lowest Temperature, City with Highest Humidity
        col1, col2, col3 = st.columns(3)
    
        with col1:
            st.metric(
                label=" City with Highest Temperature", 
                value=f"{max_temp_city_name}",
                delta=f"{max_temp_value}°C"
            )
    
        with col2:
            st.metric(
                label=" City with Lowest Temperature", 
                value=f"{min_temp_city_name}",
                delta=f"{min_temp_value}°C"
            )
    
        with col3:
            st.metric(
                label=" City with Highest Humidity", 
                value=f"{max_humidity_city_name}",
                delta=f"{max_humidity_value}%"
            )        
    
    # Plot: Weather values by city
        if not weather_df.empty:
            weather = weather_df.groupby("city_name")[selected_weather_param].mean().reset_index()
    
            fig_weather = px.bar(
                weather,
                x="city_name",
                y=selected_weather_param,
                color="city_name",
                color_discrete_map=city_color_map,
                labels={"city_name": "City", selected_weather_param.capitalize(): "Weather Value"},
                title=f" Current {selected_weather_label.capitalize()} by City"
            )
            fig_weather.update_layout(showlegend=False,xaxis_title="City",yaxis_title=f"{selected_weather_label} ({selected_unit})")
            st.plotly_chart(fig_weather, use_container_width=True)
 
else:
        st.info("No live data available. Please click 'Fetch' to load it.")
