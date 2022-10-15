from datetime import datetime
from airflow import DAG
from airflow.models.variable import Variable
from airflow.exceptions import AirflowException

config = Variable.get("variable_dag", deserialize_json = True)


def api_query(url, header, token, **kwargs):
    ti = kwargs['ti']
    print("Выполняю запрос с параметрами:")
    print("{}\n {}\n {}\n".format(url, header, token))
    count_values = 10
    ti.xcom_push(value=count_values, key='count_values')


def plus_one(starting_number):
    return starting_number + 1


def show_count(count_values):
    print(count_values)


def show_config(manual_date):
    print(manual_date)


with DAG("variable_dag", description="variable_dag",
         schedule_interval=config['start_time'],
         start_date=datetime(2021, 11, 7),
         user_defined_macros={
        "starting_number": 10,
        "plus_one" : plus_one
         },
         catchup=False) as dag:

    from airflow.operators.empty import EmptyOperator
    from airflow.operators.bash import BashOperator
    from airflow.operators.python import PythonOperator
    from airflow.providers.postgres.operators.postgres import PostgresOperator

    start_step = EmptyOperator(task_id="start_step")

    api_step = PythonOperator(task_id="api_step", python_callable=api_query,
                              op_args=[config["url"], config["header"], config["token"]])

    show_step = PythonOperator(task_id="show_step", python_callable=show_count,
                                op_args=['{{ti.xcom_pull(key = "count_values")}}'])

    config_step = PythonOperator(task_id="config_step",python_callable=show_config,
                                 op_args=["{{ dag_run.conf['manual_date'] }}"])

    bash_config_step = BashOperator(task_id="bash_config",
                                    bash_command="echo Today is {{ execution_date.format('dddd') }}")

    # !
    bash_config_2_step = BashOperator(task_id="bash_config_2",
                                    bash_command="echo Today is {{ datetime.now() }}")

    print_one = BashOperator(
        task_id="print_one",
        bash_command="echo next number from {{ starting_number }} is {{ plus_one(starting_number) }}")

    start_step >> api_step >> show_step
    start_step >> config_step
    start_step >> bash_config_step >> bash_config_2_step
    start_step >> print_one