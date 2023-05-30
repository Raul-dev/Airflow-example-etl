from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
dag_params = {
    'dag_id': '004_plsql_tables_migration',
    'start_date':datetime(2023, 5, 23),
    'schedule_interval': "@daily"
}

with DAG(**dag_params) as dag1:
    create_table_product = PostgresOperator(
        task_id='create_table_product',
        postgres_conn_id="postgres_default",
        sql='''CREATE TABLE IF NOT EXISTS public.product
            (
                product_id integer NOT NULL,
                product_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
                supplier_id integer NOT NULL,
                producttype_id integer NOT NULL,
                updated_dtm timestamp without time zone DEFAULT (CURRENT_TIMESTAMP - '6 days'::interval)
            );''',
    )
    create_table_customer = PostgresOperator(
        task_id='create_table_customer',
        postgres_conn_id="postgres_default",
        sql='''CREATE TABLE IF NOT EXISTS public.customer
            (
                customer_id character varying(16) COLLATE pg_catalog."default" NOT NULL,
                cust_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
                street character varying(50) COLLATE pg_catalog."default",
                city character varying(30) COLLATE pg_catalog."default",
                updated_dtm timestamp without time zone DEFAULT (CURRENT_TIMESTAMP - '6 days'::interval)
            );''',
    )  

with DAG(**dag_params) as dag2:
    src = PostgresHook(postgres_conn_id='postgres_oltp')
    dest = PostgresHook(postgres_conn_id='postgres_default')
    src_conn = src.get_conn()
    cursor = src_conn.cursor()
    dest_conn = dest.get_conn()
    dest_cursor = dest_conn.cursor()
    dest_cursor.execute("SELECT MAX(product_id) FROM product;")
    product_id = dest_cursor.fetchone()[0]
    if product_id is None:
        product_id = 0
    cursor.execute("SELECT * FROM product WHERE product_id > %s", [product_id])
    dest.insert_rows(table="product", rows=cursor)

    dest_cursor.execute("SELECT MAX(customer_id) FROM customer;")
    order_id = dest_cursor.fetchone()[0]
    if order_id is None:
        order_id = 0
    cursor.execute("SELECT * FROM customer WHERE customer_id > %s", [order_id])
    dest.insert_rows(table="customer", rows=cursor)
    
#    create_table_product>>create_table_customer>>migration_task     
     
