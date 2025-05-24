# Use Nginx base image
FROM nginx:alpine

# Remove default nginx page
RUN rm -rf /usr/share/nginx/html/*

# Copy custom HTML files
COPY frontend/ /usr/share/nginx/html/

# Expose port
EXPOSE 80
