from __future__ import annotations

# [START 023_CopyPlsqlToMssql]
import os
from datetime import datetime
import pytest
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
import logging
try:
    from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
    from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
except ImportError:
    pytest.skip("MSSQL provider not available", allow_module_level=True)

ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "023_CopyPlsqlToMssql"


with DAG(
    DAG_ID,
    schedule=None,
    start_date=datetime(2021, 10, 1),
    tags=["mssql"],
    catchup=False,
    #retries=0,
    #dagrun_timeout=datetime(minutes=200),
) as dag:

    create_mssql_db = MsSqlOperator(
           task_id="create_mssql_db",
            mssql_conn_id="mssql_default",
            sql=r"""CREATE DATABASE testdb;""",
            autocommit=True
    )    
    create_mssql_table = MsSqlOperator(
           task_id="create_mssql_table",
            mssql_conn_id="mssql_default",
            sql=r"""if not exists (select * from sysobjects where name='products' and xtype='U')
	CREATE TABLE products
	(
		product_id tinyint NOT NULL,
		product_name varchar(40),
		supplier_id tinyint,
		category_id tinyint,
		quantity_per_unit varchar(20),
		unit_price float,
		units_in_stock tinyint,
		units_on_order tinyint,
		reorder_level tinyint,
		discontinued int NOT NULL,
	 );""",
            database='testdb',
            autocommit=True

    )    
    
    truncate_mssql_operation = MsSqlOperator(
           task_id="truncate_products",
            mssql_conn_id="mssql_default",
            sql=r"""TRUNCATE TABLE dbo.products;""",
            database='testdb',
            autocommit=True
    )

    @dag.task(task_id="insert_mssql_hook")
    def insert_mssql_hook():
        logging.info("Startint insert.")
        logger = logging.getLogger("airflow.task")
        logger.info("Your custom error")
        src = PostgresHook(postgres_conn_id='postgres_default')
        dest = MsSqlHook(mssql_conn_id='mssql_default', schema='testdb')
        src_conn = src.get_conn()
        cursor = src_conn.cursor()
        dest_conn = dest.get_conn()
        dest_cursor = dest_conn.cursor()
        cursor.execute("SELECT * from public.products;")

        dest.insert_rows(table="products", rows=cursor)
        dest_conn.commit()
        cursor.close()
        dest_cursor.close()
        src_conn.close()
        dest_conn.close()
        logging.info("Insert data DONE.")

    (
        create_mssql_db >> create_mssql_table >> truncate_mssql_operation
        >>insert_mssql_hook()
    )

