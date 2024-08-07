# develop stage
FROM node:18-alpine as develop-stage
WORKDIR /app
COPY package*.json ./
RUN yarn global add @quasar/cli
RUN yarn install
COPY . .

# build stage
FROM develop-stage as build-stage
RUN quasar build

# production stage
FROM nginx:1.17.5-alpine as production-stage
COPY --from=build-stage /app/dist/spa /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
