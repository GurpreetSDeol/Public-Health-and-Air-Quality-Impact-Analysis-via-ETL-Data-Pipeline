
FROM python

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the ETL script and any other necessary files into the container
COPY . .
 
# Set the default command to run the ETL script
CMD ["python", "Docker_ETL_Script.py"]
