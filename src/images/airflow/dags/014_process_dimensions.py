
from __future__ import print_function
import airflow
from datetime import datetime, timedelta
from acme.operators.dwh_operators import PostgresOperatorWithTemplatedParams
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.models import Variable


args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(7),
    'provide_context': True,
    'depends_on_past': True
}

tmpl_search_path = Variable.get("sql_path")

dag = airflow.DAG(
    dag_id='014_process_dimensions',
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=60),
    template_searchpath=tmpl_search_path,
    default_args=args,
    max_active_runs=1,
    tags=["plsql"])

wait_for_cust_staging = ExternalTaskSensor(
    task_id='wait_for_cust_staging',
    external_dag_id='customer_staging',
    external_task_id='extract_customer',
    execution_delta=None,  # Same day as today
    dag=dag)

wait_for_prod_staging = ExternalTaskSensor(
    task_id='wait_for_prod_staging',
    external_dag_id='product_staging',
    external_task_id='extract_product',
    execution_delta=None,  # Same day as today
    dag=dag)

process_customer_dim = PostgresOperatorWithTemplatedParams(
    task_id='process_customer_dim',
    postgres_conn_id='postgres_dwh',
    sql='process_customer_dimension.sql',
    parameters={"window_start_date": "{{ ds }}", "window_end_date": "{{ tomorrow_ds }}"},
    dag=dag,
    pool='postgres_dwh')

process_product_dim = PostgresOperatorWithTemplatedParams(
    task_id='process_product_dim',
    postgres_conn_id='postgres_dwh',
    sql='process_product_dimension.sql',
    parameters={"window_start_date": "{{ ds }}", "window_end_date": "{{ tomorrow_ds }}"},
    dag=dag,
    pool='postgres_dwh')

wait_for_cust_staging >> wait_for_prod_staging
wait_for_prod_staging >> process_customer_dim
wait_for_prod_staging >> process_product_dim

if __name__ == "__main__":
    dag.cli()
