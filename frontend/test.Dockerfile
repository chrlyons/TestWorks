FROM node:22-alpine AS node_base

WORKDIR /frontend-app
COPY package*.json ./
RUN npm install

ENV NODE_ENV=production
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=${REACT_APP_API_URL}

COPY . .
RUN npm run build
RUN npm install -g serve
EXPOSE 3000

CMD ["serve", "-s", "build"]
