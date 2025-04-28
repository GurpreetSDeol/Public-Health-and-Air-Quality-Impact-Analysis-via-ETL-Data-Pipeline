import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc

# Title for the dashboard
st.title("🌍 Air Quality and Public Health Dashboard")

pollution_df = pd.read_csv('Streamlit Dashboard/Data/Pollution.csv')
weather_df = pd.read_csv('Streamlit Dashboard/Data/Weather.csv')
cities_df = pd.read_csv('Streamlit Dashboard/Data/Cities.csv')
who_df = pd.read_csv('Streamlit Dashboard/Data/Who Data.csv')

pollution_df['date_time'] = pd.to_datetime(pollution_df['date_time']).dt.floor('H')
weather_df['date_time'] = pd.to_datetime(weather_df['date_time']).dt.floor('H')

pollution_df['local_time'] = pd.to_datetime(pollution_df['local_time']).dt.floor('H')
weather_df['local_time'] = pd.to_datetime(weather_df['local_time']).dt.floor('H')

#  Merge df with city df 
pollution_df = pollution_df.merge(cities_df[['city_id', 'city_name']], on='city_id')
weather_df = weather_df.merge(cities_df[['city_id', 'city_name']], on='city_id')


#Sidebar settings

# Data Selection Section
city_options = cities_df['city_name'].unique().tolist()
selected_cities = st.sidebar.multiselect(
    label="Select Cities", 
    options=city_options, 
    default=city_options
)

# Date Range Selector
# Available Dates Selector
available_dates = sorted(pollution_df['local_time'].dt.date.unique())

selected_dates = st.sidebar.multiselect(
    label="Select Available Dates",
    options=available_dates,
    default=available_dates  # Default to all dates with data
)


# Pollutant Selector
pollutant_options = ['pm2_5', 'pm10', 'no2', 'o3', 'co', 'so2', 'nh3']
selected_pollutant = st.sidebar.selectbox(
    label="Select Pollutant Type",
    options=pollutant_options,
    index=0
)

# Weather Parameter Selector
weather_params = ['temperature', 'feels_like', 'humidity', 'visibility', 'wind_speed', 'clouds_all']
selected_weather_param = st.sidebar.selectbox(
    label="Select Weather Parameter",
    options=weather_params,
    index=0
)


# Sidebar for selecting multiple causes of death
cause_options = who_df['cause'].unique().tolist()
selected_causes = st.sidebar.multiselect(
    label="Select Causes of Death", 
    options=cause_options, 
    default=cause_options  # Default to all causes
)


#City Section

st.subheader("📊 Key Population Insights")
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
        label="🌆 Most Populated City", 
        value=highest_city_name, 
        delta=f"Population: {highest_city_population:,}"
    )

with col2:
    st.metric(
        label="🗺️ National Population", 
        value=country_name, 
        delta=f"Population: {national_population:,}"
    )

st.divider()

st.subheader("🗺️ 2D Map: Cities by Population Size")
st.write("Each city is represented based on its geographic location. Marker size and color intensity reflect population.")
st.plotly_chart(fig)

st.divider()


# Pollution Section


st.subheader("💨 Pollution Insights")
st.write("This section visualizes the pollution levels of various pollutants such as PM2.5, PM10, NO2, O3, CO, SO2, and NH3 across selected cities. You can explore how pollutant levels change over time and their relationship with city population.")


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

# Define color palette for cities
city_colors = pc.qualitative.Plotly

#  Plot the first graph: Avg pollutant by city over 24 hours
fig_avg_24h_city = px.line(
    avg_pollutant_by_city_hour,
    x='hour_of_day',
    y=selected_pollutant,
    color='city_name', 
    markers=True,
    color_discrete_map={city_name: color for city_name, color in zip(cities_df['city_name'].unique(), city_colors)},
    labels={
        'hour_of_day': 'Hour of Day',
        selected_pollutant: f'Avg {selected_pollutant.upper()}',
        'city_name': 'City'
    },
    title=f"Average {selected_pollutant.upper()} Levels Throughout the Day (by City)"
)

fig_avg_24h_city.update_layout(
    xaxis=dict(tickmode='linear', tick0=0, dtick=1),
    yaxis_title=f"{selected_pollutant.upper()} Concentration (µg/m³)",
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
        'title': f"Comparison of Average {selected_pollutant.upper()} Levels and Population Across Cities",
        'yaxis': {'title': f'Avg {selected_pollutant.upper()} (µg/m³)'},
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
        label=f"🏙️ City with Highest Average {selected_pollutant.upper()} Pollution", 
        value=max_avg_pollution_city_name,
        delta=f"{max_avg_pollution_value:.2f} µg/m³"
    )

with col2:
    st.metric(
        label=f"🏙️ City with Highest {selected_pollutant.upper()} Pollution", 
        value=max_pollution_city_name,
        delta=f"{max_pollution_value:.2f} µg/m³"
    )

with col3:
    st.metric(
        label=f"⏰ Hour with Highest {selected_pollutant.upper()} Pollution", 
        value=max_pollution_hour_time,
        delta=f"{max_pollution_hour_value:.2f} µg/m³"
    )

# Display the First and Second Pollution Plots
st.plotly_chart(fig_avg_24h_city)
st.plotly_chart(fig_bar_comparison)



# --- Weather Section


st.subheader("🌤️ Weather Insights")
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
    color_discrete_map={city_name: color for city_name, color in zip(cities_df['city_name'].unique(), city_colors)},
    labels={
        'hour_of_day': 'Hour of Day',
        selected_weather_param: f'Avg {selected_weather_param.capitalize()}',
        'city_name': 'City'
    },
    title=f"Average {selected_weather_param.capitalize()} Throughout the Day (by City)"
)

fig_avg_24h_weather.update_layout(
    xaxis=dict(tickmode='linear', tick0=0, dtick=1),
    yaxis_title=f"{selected_weather_param.capitalize()}",
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
    color_discrete_map={city_name: color for city_name, color in zip(cities_df['city_name'].unique(), city_colors)},
    labels={
        'city_name': 'City',
        selected_weather_param: f"Avg {selected_weather_param.capitalize()}"
    },
    title=f"Comparison of Average {selected_weather_param.capitalize()} Across Cities"
)

fig_bar_weather_comparison.update_layout(
    yaxis_title=f"Avg {selected_weather_param.capitalize()}",
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
        label="🌡️ City with Highest Temperature", 
        value=f"{max_temp_city_name}",
        delta=f"{max_temp_value}°C"
    )

with col2:
    st.metric(
        label="❄️ City with Lowest Temperature", 
        value=f"{min_temp_city_name}",
        delta=f"{min_temp_value}°C"
    )

with col3:
    st.metric(
        label="💧 City with Highest Humidity", 
        value=f"{max_humidity_city_name}",
        delta=f"{max_humidity_value}%"
    )

st.divider()


# Display the First and Second Weather Plots
st.plotly_chart(fig_avg_24h_weather)
st.plotly_chart(fig_bar_weather_comparison)



# WHO data section



st.subheader("🌍 WHO Data Insights")
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
        label="💔 City with Highest Total Deaths", 
        value=f"{max_total_deaths_city_name}",
        delta=f"{max_total_deaths} deaths"
    )

with col2:
    st.metric(
        label="💚 City with Lowest Total Deaths", 
        value=f"{min_total_deaths_city_name}",
        delta=f"{min_total_deaths} deaths"
    )

st.divider()


# Display the chart
st.plotly_chart(fig_deaths_by_cause_100k)
