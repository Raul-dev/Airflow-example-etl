from datetime import datetime, timedelta
from airflow import DAG
import logging
from airflow.operators.empty import EmptyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator

dag_params = {
    
    'start_date':datetime(2023, 5, 23),
    'schedule_interval': None
}

with DAG(
    dag_id='024_sql_utf8',
    default_args=dag_params,
    tags=["mssql"],
) as dag:

    @dag.task(task_id="Инициализация")
    def migration_task():
        logging.info("Startintg хочу по русски .")

    create_db1=PostgresOperator(
            task_id='create_db1',
            postgres_conn_id="mssql_default",
            sql='''
            IF DB_ID('client1_ods') IS NULL
            BEGIN
                print 'Создаем базу client1_dwh' 
                CREATE DATABASE client1_ods;
            END
            ''',
            autocommit=True,
        )
    create_db2=PostgresOperator(
            task_id='create_db2',
            postgres_conn_id="mssql_default",
            sql='''
            IF DB_ID('client1_dwh') IS NULL
            BEGIN
                print 'Создаем базу client1_dwh' 
                CREATE DATABASE client1_dwh;
            END
            ''',
            autocommit=True,
        )            
        

    create_table_postgres = PostgresOperator(
        task_id='create_table_postgres',
        postgres_conn_id="postgres_default",
        sql='''CREATE TABLE IF NOT EXISTS public.порусскихочу
            (
                product_id integer NOT NULL,
                а_вот_так_клиент_хочет character varying(50) COLLATE pg_catalog."default" NOT NULL,
                клиент_должен_быть_счастлив int
            );''',
    )

    mssql_create_table = MsSqlOperator(
        task_id='mssql_create_table',
        mssql_conn_id='mssql_default',
        sql="""if not exists(select 1 from sysobjects where name =N'Новаятаблица')
            CREATE TABLE [Новаятаблица] (
                гудбай_америка int
            )
            """,
        database='client1_dwh',
        autocommit=True,
    )
 
    select_mssql = MsSqlOperator(task_id='select_mssql',
        mssql_conn_id='mssql_default',
        sql='''SELECT * FROM [Новаятаблица]''',
        database='client1_dwh',
        autocommit=True,
    )

    @dag.task(task_id="bulk_insert")
    def bulk_insert():
        
        src = MsSqlHook(mssql_conn_id='mssql_default', schema='client1_dwh')
        src_conn = src.get_conn()
        cursor = src_conn.cursor()
        cursor.execute("""SELECT 'тест' as gg """)
        cursor.close()
        src_conn.close()
        logging.info("Завершение.")

migration_task()>>[create_db1,create_db2]>>create_table_postgres>>mssql_create_table>>select_mssql>>bulk_insert()