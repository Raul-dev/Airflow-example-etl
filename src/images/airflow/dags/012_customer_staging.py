from __future__ import print_function
import airflow
from datetime import datetime, timedelta
from acme.operators.dwh_operators import PostgresToPostgresOperator
from acme.operators.dwh_operators import AuditOperator
from airflow.models import Variable


args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(7),
    'provide_context': True
}

tmpl_search_path = Variable.get("sql_path")

dag = airflow.DAG(
    dag_id='012_customer_staging',
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=60),
    template_searchpath=tmpl_search_path,
    default_args=args,
    max_active_runs=1,
    tags=["plsql"])

get_auditid = AuditOperator(
    task_id='get_audit_id',
    postgres_conn_id='postgres_dwh',
    audit_key="customer",
    cycle_dtm="{{ ts }}",
    dag=dag,
    pool='postgres_dwh')

extract_customer = PostgresToPostgresOperator(
    sql='select_customer.sql',
    pg_table='staging.customer',
    src_postgres_conn_id='postgres_oltp',
    dest_postgress_conn_id='postgres_dwh',
    pg_preoperator="DELETE FROM staging.customer WHERE "
        "partition_dtm >= DATE '{{ ds }}' AND partition_dtm < DATE '{{ tomorrow_ds }}'",
    parameters={"window_start_date": "{{ ds }}", "window_end_date": "{{ tomorrow_ds }}",
                "audit_id": "{{ ti.xcom_pull(task_ids='get_audit_id', key='audit_id') }}"},
    task_id='extract_customer',
    dag=dag,
    pool='postgres_dwh')

get_auditid >> extract_customer


if __name__ == "__main__":
    dag.cli()
