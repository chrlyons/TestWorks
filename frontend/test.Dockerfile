FROM node:21-alpine AS node_base

WORKDIR /frontend-app
COPY package*.json ./
RUN npm install

ENV NODE_ENV=production

COPY . .
RUN npm run build
RUN npm install -g serve
EXPOSE 3000

CMD ["serve", "-s", "build"]
