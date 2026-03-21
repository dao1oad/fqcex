FROM node:22-alpine AS build

WORKDIR /app

COPY . /app

RUN npm --prefix apps/control-plane-ui install \
    && npm --prefix apps/control-plane-ui run build

FROM nginx:1.29-alpine

COPY deploy/operator-ui.nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/apps/control-plane-ui/dist /usr/share/nginx/html
