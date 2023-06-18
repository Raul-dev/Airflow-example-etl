
from __future__ import print_function
import airflow
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow import models
from airflow.settings import Session
import logging


args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(7),
    'provide_context': True
}


def initialize_etl_example():
    logging.info('Creating connections, pool and sql path')

    session = Session()

    def create_new_conn(session, attributes):
        new_conn = models.Connection()
        new_conn.conn_id = attributes.get("conn_id")
        new_conn.conn_type = attributes.get('conn_type')
        new_conn.host = attributes.get('host')
        new_conn.port = attributes.get('port')
        new_conn.schema = attributes.get('schema')
        new_conn.login = attributes.get('login')
        new_conn.set_password(attributes.get('password'))

        session.add(new_conn)
        session.commit()

    create_new_conn(session,
                    {"conn_id": "oracle_con",
                     "conn_type": "oracle",
                     "host": "xedatabase",
                     "port": 1521,
                     "schema": "XEPDB1",
                     "login": "dbo",
                     "password": "password"})

    create_new_conn(session,
                    {"conn_id": "oracle_system",
                     "conn_type": "oracle",
                     "host": "xedatabase",
                     "port": 1521,
                     "schema": "XEPDB1",
                     "login": "system",
                     "password": "password"})


    session.commit()
    session.close()

dag = airflow.DAG(
    dag_id='040_oracle_init_connection',
    schedule_interval= None, #"@once",
    default_args=args,
    max_active_runs=1,
    tags=["oracle"]
)

ti = PythonOperator(
    task_id="initialize_etl_example",
    python_callable=initialize_etl_example,
    dag=dag,
)

ti