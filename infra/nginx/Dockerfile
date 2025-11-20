# Build from root!
FROM nginx:alpine

# Remove default nginx website
RUN rm /etc/nginx/conf.d/default.conf

# Copy the custom nginx configuration file
COPY infra/nginx/nginx.conf /etc/nginx/conf.d

# Copy static file
COPY entry_point/app/static /static