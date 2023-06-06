FROM apache/airflow:2.6.1
EXPOSE 443
# Use root user for installation
USER root


## Setup MSSQL driver
RUN apt-get update -y && apt-get update \
  && apt-get install -y --no-install-recommends curl gcc g++ gnupg unixodbc-dev

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update

# install SQL Server drivers
RUN ACCEPT_EULA=Y apt-get install msodbcsql17 -y

# install SQL Server tools
RUN ACCEPT_EULA=Y apt-get install mssql-tools -y \
  && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile \
  && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

RUN mkdir -p /srv/https
COPY ./srv/nginx/certs/host.docker.internal.crt /srv/https/host.docker.internal.crt
COPY ./srv/nginx/certs/host.docker.internal.key /srv/https/host.docker.internal.key
    
    

USER airflow

RUN pip install pyodbc pymssql==2.2.7 psycopg2-binary
RUN pip install apache-airflow-providers-microsoft-mssql
RUN pip install -U pytest
RUN pip install pytest-watcher
# ml modules
#RUN pip install matplotlib
#RUN pip install xgboost
#RUN pip install tensorflow
#RUN pip install numpy
#RUN pip install jupyterlab
#RUN pip install jupyter
#RUN pip install papermill
#RUN pip install torch torchvision torchaudio
#RUN pip install fastai

# New entrypoint script
#COPY init_db_and_start.sh /
#RUN chmod +x /init_db_and_start.sh

# Set airflow home
ENV AIRFLOW_HOME=/opt/airflow


#COPY airflow.cfg $AIRFLOW_HOME/airflow.cfg
# RUN touch unittests.cfg
# RUN touch /usr/local/airflow/airflow.cfg
#ENTRYPOINT [ "bash",  "/init_db_and_start.sh" ]
