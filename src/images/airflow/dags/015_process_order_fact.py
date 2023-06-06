
from __future__ import print_function
import airflow
from datetime import datetime, timedelta
from acme.operators.dwh_operators import PostgresOperatorWithTemplatedParams
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.models import Variable


args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(7),
    'provide_context': True
}

tmpl_search_path = Variable.get("sql_path")

dag = airflow.DAG(
    dag_id='015_process_order_fact',
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=60),
    template_searchpath=tmpl_search_path,
    default_args=args,
    max_active_runs=1,
    tags=["plsql"])

wait_for_prod_dims = ExternalTaskSensor(
    task_id='wait_for_proc_dims',
    external_dag_id='process_dimensions',
    external_task_id='process_product_dim',
    execution_delta=None,  # Same day as today
    dag=dag)

wait_for_cust_dims = ExternalTaskSensor(
    task_id='wait_for_cust_dims',
    external_dag_id='process_dimensions',
    external_task_id='process_customer_dim',
    execution_delta=None,  # Same day as today
    dag=dag)

process_order_fact = PostgresOperatorWithTemplatedParams(
    task_id='process_order_fact',
    postgres_conn_id='postgres_dwh',
    sql='process_order_fact.sql',
    parameters={"window_start_date": "{{ ds }}", "window_end_date": "{{ tomorrow_ds }}"},
    dag=dag,
    pool='postgres_dwh')

wait_for_cust_dims >> wait_for_prod_dims
wait_for_prod_dims >> process_order_fact

if __name__ == "__main__":
    dag.cli()
