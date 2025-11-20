FROM nginx:alpine

# Remove default nginx website
RUN rm /etc/nginx/conf.d/default.conf

# Copy the custom nginx configuration file
COPY nginx/nginx.conf /etc/nginx/conf.d

# Copy static files from the app container
COPY ./app/static /usr/share/nginx/html/static/