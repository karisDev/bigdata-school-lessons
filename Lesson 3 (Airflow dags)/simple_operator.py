import datetime
from airflow import DAG


def square(k):
    print(k*k)


with DAG("simple_operators", description="simple_operators",
         schedule_interval="@daily",
         start_date=datetime.datetime(2021, 11, 7),
         catchup=False) as dag:

    from airflow.operators.empty import EmptyOperator
    from airflow.operators.bash import BashOperator
    from airflow.operators.python import PythonOperator
    from airflow.providers.postgres.operators.postgres import PostgresOperator

    start_step = EmptyOperator(task_id="start_step")

    bash_step = BashOperator(task_id="bash_step", bash_command="echo $(date -d \"$(date +%Y-%m-01) -1 day\" +%Y-%m-%d)")

    python_step = PythonOperator(task_id="python_step", python_callable=square, op_args=[3])

    postgres_step = PostgresOperator(task_id="postgres_step", postgres_conn_id="mars_test",
                                     sql= "SELECT max(value) FROM dds_stg.table_with_value")

    postgres_step2 = PostgresOperator(task_id="postgres_step2",
                                      postgres_conn_id="mars_test",
                                      sql="""INSERT INTO dds_stg.table_with_value
                                             (id, value) VALUES (13, 13)                                  
                                             """)

# load_step = BashOperator(task_id ='load_step',
#                        bash_command ='python3 {}scripts/load_step.py'.format(DIRRECTORY_OF_SCRIPTS),
#                         env = {"ORACLE_HOME": "/opt/oracle/instantclient_21_5",
#                                "LD_LIBRARY_PATH" : "/opt/oracle/instantclient_21_5"})


#    send_email = EmailOperator(
#        task_id='send_email',
#        to='test@gmail.com',
#        subject='ingestion complete',
#        html_content="hello")

start_step >> bash_step
start_step >> python_step
start_step >> postgres_step >> postgres_step2