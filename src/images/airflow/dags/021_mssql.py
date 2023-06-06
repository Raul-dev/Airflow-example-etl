# this is not production code. just useful for testing connectivity.
import datetime as dt
import time
import pytest
from airflow import DAG
try:
    from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
    from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
except ImportError:
    pytest.skip("MSSQL provider not available", allow_module_level=True)


args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2019, 11, 8, 23, 00, 00),
    'concurrency': 1,
    'retries': 0
}

dag = DAG(
    dag_id="021_mssql_example",
    default_args=args,
    schedule_interval=None,
    start_date=dt.datetime(2020, 1, 1),
    tags=["mssql"],
)


sql_command = """SELECT @@SERVERNAME AS 'Server Name', @@VERSION AS 'Server Version';"""
t1 = MsSqlOperator(task_id='selecting_server_name',
                   mssql_conn_id='mssql_default',
                   sql=sql_command,
                   dag=dag,
                   database='master',
                   autocommit=True)
t1