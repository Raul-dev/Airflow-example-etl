ARG postgres_version=14
#FROM postgres:$postgres_version
FROM postgis/postgis:14-3.3
ARG oracle_fdw_version=2_5_0
ARG instantclient_version=21_10

RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    libaio1 \
    libaio-dev \
    build-essential \
    make \
    unzip \
    postgresql-server-dev-14 \
    postgresql-common
	
RUN mkdir /test
COPY sdk\ /tmp

RUN unzip "/tmp/*.zip" -d /tmp

ENV ORACLE_HOME /tmp/instantclient_${instantclient_version}
ENV LD_LIBRARY_PATH /tmp/instantclient_${instantclient_version}
RUN cd /tmp/oracle_fdw-ORACLE_FDW_${oracle_fdw_version} && make && make install
RUN cd /tmp && cc -I/usr/include/postgresql/14/server/ -fpic -c /tmp/math3d.c
RUN cd /tmp && cc -shared -L/usr/lib/postgresql/14/lib -lpq -o math3d.so math3d.o
RUN cd /tmp && cp math3d.so /usr/lib/postgresql/14/lib    

RUN cd /tmp &&  cp math3d.control /usr/share/postgresql/14/extension/
RUN cd /tmp &&  cp math3d--1.0.sql /usr/share/postgresql/14/extension/

USER postgres

ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 5432
CMD ["postgres"]