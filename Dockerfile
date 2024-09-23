
FROM python

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the ETL script and any other necessary files into the container
COPY Data_ETL/Weather_and_pollution_ETL_script.py .
COPY Data_ETL/.env .
COPY Data_ETL/Final_city_data.json .
 
# Set the default command to run the ETL script
CMD ["python", "Weather_and_pollution_ETL_script.py"]
