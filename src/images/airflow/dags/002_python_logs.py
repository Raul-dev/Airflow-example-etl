from pprint import pprint
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import logging


dag = DAG(
    dag_id='002_python_logs',
    start_date=datetime(2022, 5, 28),
    schedule_interval=None
)

def loginfo1(logtext,**kwargs):
#logtext,**kwargs    
    logging.info('DAG loging: %s', logtext)
    pprint(kwargs)
    print(logtext)

start_task = PythonOperator(
        task_id='start',
        python_callable=loginfo1,
        op_kwargs={"logtext":'start msg'},
        dag=dag,
    )

print_hello_world = BashOperator(
        task_id='print_hello_world',
        bash_command='echo "HelloWorld!"'
    )

end_task = PythonOperator(
        task_id='end',
        python_callable=loginfo1,
        op_kwargs={"logtext":'end msg'},
        dag=dag,
    )

start_task >> print_hello_world
print_hello_world >> end_task
