
FROM python

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the ETL script and any other necessary files into the container
COPY Data_ETL/Weather_and_pollution_ETL_script.py .
COPY Data_ETL/Data_Files/config.json .
COPY Data_ETL/Data_Files/Final_city_data.json .
COPY Data_ETL/Data_Files/Final_city_data.csv .
COPY Data_ETL/SQL_Files/Database_Creation.sql .
COPY Data_ETL/SQL_Files/Populate_Cities_Table.sql .
COPY Data_ETL/SQL_Files/Update_Fact_Table.sql . 

# Set the default command to run the ETL script
CMD ["python", "Weather_and_pollution_ETL_script.py"]
