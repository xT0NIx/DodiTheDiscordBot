# Use an official Python runtime for ARM architecture
FROM arm32v7/python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY main.py requirements.txt .env /app/

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y \
        gcc \
        libffi-dev \
        libssl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc libffi-dev libssl-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /tmp/*

# Make port 80 available to the world outside this container
EXPOSE 80

# Run your application
CMD ["python", "main.py"]
