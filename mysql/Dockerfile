FROM mysql:8


ENV MYSQL_ROOT_PASSWORD="root"

EXPOSE 3306 3306
COPY ./mysql-volume/init/init.sql /data/application/init.sql
VOLUME ./mysql-volume/data /var/lib/mysql



CMD ["mysqld", "--init-file", "/data/application/init.sql"]

