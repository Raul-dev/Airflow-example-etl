https://www.postgresql.fastware.com/postgresql-insider-fdw-ora-bas
https://github.com/laurenz/oracle_fdw
https://github.com/mfvitale/postgres-oracle-fdw/blob/master/Dockerfile

создание расширений
https://habr.com/ru/articles/198332/

Copy `oracle_fdw.dll` into the PostgreSQL library directory and 
copy `oracle_fdw.control` and the SQL files into the `extension` 
subdirectory of the PostgreSQL share directory.  
To find those directories, you can use `pg_config --libdir` and 
pg_config --sharedir
pg_config --pkglibdir
pg_config --version

/usr/share/postgresql/14

docker build -t postgres-ora-fdw .
docker stop test-postgres
docker rm test-postgres
docker run -d -p 5432:5432 -v ./test:/test -e POSTGRES_PASSWORD=password -e POSTGRES_HOST_AUTH_METHOD=trust --name test-postgres   postgres-ora-fdw
docker run -d -p 5432:5432 -v ./test:/test -e POSTGRES_PASSWORD=password -e POSTGRES_HOST_AUTH_METHOD=trust --name test-postgres   postgis/postgis:14-3.3

docker exec -it --user root <container_id> /bin/bash

cat /usr/share/postgresql/14/extension/oracle_fdw.control

#install oracle_fdw
    && wget -O /tmp/instantclient-basic.zip  https://download.oracle.com/otn_software/linux/instantclient/19600/instantclient-basiclite-linux.x64-"${ORACLE_VERSION}"dbru.zip \
    && wget -O /tmp/instantclient-sdk.zip  https://download.oracle.com/otn_software/linux/instantclient/19600/instantclient-sdk-linux.x64-"${ORACLE_VERSION}"dbru.zip \
    && unzip /tmp/instantclient-basic.zip -d /tmp/Oracle \
    && unzip /tmp/instantclient-sdk.zip -d /tmp/Oracle \
    && mv /tmp/Oracle/"${ORACLE_DIR_NAME}" /Oracle \
    && rm -f /Oracle/ojdbc8.jar /Oracle/ucp.jar /Oracle/xstreams.jar \
    && wget -O /tmp/oracle_fdw.zip  https://github.com/laurenz/oracle_fdw/archive/ORACLE_FDW_"${ORACLE_FDW_VERSION}".zip \
    && unzip /tmp/oracle_fdw.zip  -d /tmp \
    && cd /tmp/oracle_fdw-ORACLE_FDW_"${ORACLE_FDW_VERSION}" \
    && make USE_PGXS=1 install \

create extension oracle_fdw;

https://www.postgresql.fastware.com/postgresql-insider-fdw-ora-bas
CREATE SERVER ora_sv FOREIGN DATA WRAPPER oracle_fdw OPTIONS (dbserver 'xedatabase:1521/XEPDB1');
CREATE USER MAPPING FOR postgres SERVER ora_sv OPTIONS ( USER 'system', PASSWORD 'password');
CREATE FOREIGN TABLE f_ora_tbl(
id int OPTIONS (key 'true'), 
name varchar(64),
t_data timestamp)
SERVER ora_sv OPTIONS (SCHEMA 'DBO' , TABLE 'TABLE1'); 
DROP FOREIGN TABLE f_ora_tbl;

SELECT * FROM f_ora_tbl
