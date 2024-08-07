# Develop stage
FROM node:18-alpine as develop-stage
WORKDIR /app

# Install Quasar CLI globally
RUN npm install -g @quasar/cli

# Copy dependency files
COPY package.json package-lock.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build stage
FROM node:18-alpine as build-stage
WORKDIR /app

# Install Quasar CLI globally
RUN npm install -g @quasar/cli

# Copy dependency files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the entire application code
COPY . .

# Build the application
RUN quasar build

# Production stage
FROM nginx:1.21-alpine as production-stage

# Copy the built files from the build stage
COPY --from=build-stage /app/dist/spa /usr/share/nginx/html

# Copy Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 for the application
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
