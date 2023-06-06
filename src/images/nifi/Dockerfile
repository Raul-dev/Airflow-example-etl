FROM apache/nifi
USER root
RUN mkdir /lib/jdbc
WORKDIR /lib/jdbc
RUN wget https://go.microsoft.com/fwlink/?linkid=2222954
RUN tar xvzf sqljdbc_12.2.0.0_enu.tar.gz
RUN cp ./sqljdbc_12.2/enu/mssql-jdbc-12.2.0.jre8.jar ./

USER nifi

COPY flow.xml.gz /opt/nifi/nifi-current/conf/flow.xml.gz

EXPOSE 8080 8443 10000 8000

WORKDIR ${NIFI_HOME}
ENTRYPOINT ["../scripts/start.sh"]