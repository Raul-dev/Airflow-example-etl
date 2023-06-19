from airflow import DAG
import logging
from airflow.utils.task_group import TaskGroup
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.utils.timezone import make_naive


with DAG(
    dag_id='030_Trigger_DagRun',
    tags=["Trigger"],
    start_date=make_naive(days_ago(1)),
    schedule=None,
    schedule_interval=None,
) as dag:

    @dag.task(task_id="Инициализация")
    def initial_task():
        logging.info("Startintg хочу по русски .")

    task1 = TriggerDagRunOperator(
        task_id='Run_001_Hello_world',
        trigger_dag_id='001_Hello_world',
	    wait_for_completion=True
    )
  
    task2 = TriggerDagRunOperator(
        task_id='Run_002_python_logs',
        trigger_dag_id='002_python_logs',
	    wait_for_completion=True
    )
  

initial_task()>>[task1,task2]