FROM nginx:latest
WORKDIR /usr/src/app
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./static /usr/src/app/staticfiles
COPY ./media /usr/src/app/media
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
