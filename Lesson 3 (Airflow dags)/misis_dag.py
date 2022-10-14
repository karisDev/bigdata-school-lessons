from datetime import datetime
from airflow.models.variable import Variable
from airflow import DAG

config = Variable.get("karis_vars", deserialize_json = True)

def print_hello(times:int):
    print(" Hello " * times)

with DAG(config["dag_name"],
    schedule_interval="1 * * * *",
    description="Misis test",
    catchup=False,
    start_date=datetime(2022, 10, 8)) as dag:

    from airflow.operators.empty import EmptyOperator
    from airflow.operators.bash import BashOperator
    from airflow.operators.python_operator import PythonOperator
    start_step = EmptyOperator(task_id="empty_step")
    hello_step = BashOperator(task_id="print_hello", bash_command="echo hello")
    python_step = PythonOperator(task_id="python_hello",
                                 python_callable=print_hello,
                                 op_args=[config["times"]])

start_step >> hello_step
start_step >> python_step