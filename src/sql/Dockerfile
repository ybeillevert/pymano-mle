FROM mysql/mysql-server:5.7

ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=4dm1n!
ENV MYSQL_DATABASE=pymanoDB

COPY ./init.sql /docker-entrypoint-initdb.d/
EXPOSE 3306