import uuid
from datetime import datetime
from airflow import DAG
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.postgres_operator import PostgresOperator


dag_params = {
    'dag_id': '003_plsql_insert',
    'start_date': datetime(2023, 5, 7),
    'schedule_interval': None,
    'tags':["Simple postgres example"],

}


with DAG(**dag_params) as dag:

    drop_table = PostgresOperator(
        task_id='drop_table',
        postgres_conn_id="postgres_default",
        sql='''DROP TABLE IF EXISTS new_table;''',
    )

    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id="postgres_default",
        sql='''CREATE TABLE new_table(
            custom_id integer NOT NULL, 
            timestamp TIMESTAMP NOT NULL, 
            user_id VARCHAR (50) NOT NULL
            );''',
    )

    insert_row = PostgresOperator(
        task_id='insert_row',
        postgres_conn_id="postgres_default",
        sql='INSERT INTO new_table VALUES(%s, %s, %s)',
        trigger_rule=TriggerRule.ALL_DONE,
        parameters=(uuid.uuid4().int % 123456789, datetime.now(), uuid.uuid4().hex[:10])
    )
    create_table_product = PostgresOperator(
        task_id='create_table_product',
        postgres_conn_id="postgres_default",
        sql='''CREATE TABLE IF NOT EXISTS products (
            product_id smallint NOT NULL PRIMARY KEY,
            product_name character varying(40) NOT NULL,
            supplier_id smallint,
            category_id smallint,
            quantity_per_unit character varying(20),
            unit_price real,
            units_in_stock smallint,
            units_on_order smallint,
            reorder_level smallint,
            discontinued integer NOT NULL
        );''',
    )
    create_table_customer = PostgresOperator(
        task_id='create_table_orders',
        postgres_conn_id="postgres_default",
        sql='''CREATE TABLE IF NOT EXISTS orders (
            order_id smallint NOT NULL PRIMARY KEY,
            customer_id bpchar,
            employee_id smallint,
            order_date date,
            required_date date,
            shipped_date date,
            ship_via smallint,
            freight real,
            ship_name character varying(40),
            ship_address character varying(60),
            ship_city character varying(15),
            ship_region character varying(15),
            ship_postal_code character varying(10),
            ship_country character varying(15)
        );''',
    )  
    drop_table>>create_table >> insert_row