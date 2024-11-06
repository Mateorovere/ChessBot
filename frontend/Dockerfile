# Frontend Dockerfile
FROM node:16

# Set the working directory
WORKDIR /app

# Copy the frontend code
COPY . /app

# Install dependencies
RUN npm install

# Expose the port React runs on
EXPOSE 3000

# Command to start the React application
CMD ["npm", "start"]
