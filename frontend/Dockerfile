# ───── Build stage ─────
FROM node:18-alpine AS build

# 1) Declare the build‐arg
ARG REACT_APP_API_URL

# 2) Export it so Create React App will embed it
ENV REACT_APP_API_URL=${REACT_APP_API_URL}

WORKDIR /app
COPY package*.json ./
# You said you use `npm install`:
RUN npm install

COPY . .
RUN npm run build

# ───── Serve stage ─────
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
