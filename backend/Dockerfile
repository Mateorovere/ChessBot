FROM python:3.11

# Set the working directory
WORKDIR /app

# Install Stockfish
RUN apt-get update && apt-get install -y stockfish

# Copy the backend code
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
