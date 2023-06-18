from __future__ import annotations

import os
from datetime import datetime
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
import logging
from airflow.providers.oracle.hooks.oracle import OracleHook
from airflow.providers.oracle.operators.oracle import OracleOperator

ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "041_OracleCreateUser"


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
            task_id="oracle_test_operation",
            oracle_conn_id="oracle_system",
            sql=r"""   
                declare
                nCount number;
                v_sql clob;
                begin
                    select count(*) into nCount from all_users WHERE USERNAME = 'DBO';
                    if nCount <= 0 then
                        v_sql := '
                        create user dbo IDENTIFIED BY password';
                        execute immediate v_sql;

                        v_sql := '
                        grant create any table to dbo';
                        execute immediate v_sql;

                        v_sql := '
                        grant dba to dbo';
                        execute immediate v_sql;

                    end if;
                    
                    select count(*) into nCount from dba_tables where table_name = 'TABLE0';

                    if nCount <= 0 then
                        v_sql := '
                        CREATE table dbo.table0(
                                id number
                        )';

                        execute immediate v_sql;

                    end if;
                end;             
            """,
    )
    oracle_select_operation = OracleOperator(
            task_id="oracle_select_operation",
            oracle_conn_id="oracle_con",
            sql="""SELECT * FROM dbo.TABLE0
            """,
    )

    (
        oracle_create_operation>>oracle_select_operation
    )

