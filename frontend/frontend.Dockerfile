# Use the official Nginx image as the base image
FROM nginx:alpine

# Copy the frontend HTML and assets to the Nginx directory
COPY frontend/ /usr/share/nginx/html/

# Copy the custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose the port Nginx runs on
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]