from __future__ import annotations
from datetime import datetime
#import pytest
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
import logging
from airflow.providers.oracle.hooks.oracle import OracleHook
from airflow.providers.oracle.operators.oracle import OracleOperator


DAG_ID = "042_OraclePostgresEtl"


with DAG(
    DAG_ID,
    schedule=None,
    start_date=datetime(2021, 10, 1),
    tags=["oracle"],
    catchup=False,
    #retries=0,
    #dagrun_timeout=datetime(minutes=200),
) as dag:
    
    oracle_create_operation = OracleOperator(
        task_id="oracle_create_operation",
        oracle_conn_id="oracle_con",
        sql="""    
            declare
            nCount number;
            v_sql clob;
            begin
                select count(*) into nCount from dba_tables where table_name = 'TABLE1';

                if ncount <= 0 then
                    v_sql := '
                    CREATE table dbo.table1(
                            id number
                    )';

                    execute immediate v_sql;

                end if;
            end;
        """,
    )
    oracle_insert_operation = OracleOperator(
        task_id="oracle_insert_operation",
        oracle_conn_id="oracle_con",
        sql=r"""INSERT INTO dbo.TABLE1 (id) VALUES (1)""",
    )
    create_table_operation = PostgresOperator(
        task_id="create_table_operation",
        postgres_conn_id="postgres_default",
        sql='''CREATE TABLE IF NOT EXISTS public.table1
            (
                id numeric(38,0)
            );''',
        
    )
    truncate_operation = PostgresOperator(
        task_id="truncate_operation",
        postgres_conn_id="postgres_default",
        sql=r"""TRUNCATE TABLE public.table1;""",
    )
    
    @dag.task(task_id="insert_psql_hook")
    def insert_psql_hook():
        logging.info("Startintg insert.")
        src = OracleHook(oracle_conn_id='oracle_con')
        dest = PostgresHook(postgres_conn_id='postgres_default') 
#        dest = PostgresHook(postgres_conn_id='postgres_metastorage')
        src_conn = src.get_conn()
        cursor = src_conn.cursor()
        dest_conn = dest.get_conn()
        dest_cursor = dest_conn.cursor()
        cursor.execute("SELECT * FROM dbo.TABLE1")
#        dest.insert_rows(table="metadata", rows=cursor, replace=True, replace_index="nkey")
        dest.insert_rows(table="TABLE1", rows=cursor)
        dest_conn.commit()
        cursor.close()
        dest_cursor.close()
        src_conn.close()
        dest_conn.close()
        logging.info("insert data DONE.")        

    (
       [oracle_create_operation,create_table_operation]>>oracle_insert_operation>>truncate_operation>>insert_psql_hook()
    )

