FROM node:alpine3.17

# Set local timezone
RUN apk add --no-cache tzdata
ENV TZ=Asia/Kuala_Lumpur

# Add a work directory
WORKDIR /app
# Cache and Install dependencies
COPY package.json .
COPY yarn.lock .
RUN yarn install
# Copy app files
COPY . .
# RUN yarn build
# Expose port
EXPOSE 3000