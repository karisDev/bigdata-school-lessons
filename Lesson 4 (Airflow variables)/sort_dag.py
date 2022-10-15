from datetime import datetime
from airflow import DAG
from airflow.models.variable import Variable

config = Variable.get("array_example", deserialize_json = True)

def sort_list(list_to_sort, **kwargs):
  ti = kwargs['ti']
  ti.xcom_push(value=sorted(list_to_sort), key='sorted_list')

with DAG('sort_list',
  description='Sort list DAG',
  schedule_interval='0 12 * * *',
  start_date=datetime(2017, 3, 20), catchup=False) as dag:
  
  from airflow.operators.empty import EmptyOperator
  from airflow.operators.python_operator import PythonOperator
  from airflow.operators.bash import BashOperator

  start_step = EmptyOperator(task_id="start_step")
  sort_list = PythonOperator(task_id='sort_list', python_callable=sort_list, op_args=[config["arr"]], dag=dag)
  print_list = BashOperator(task_id='print_list', bash_command='echo {{ ti.xcom_pull(key = "sorted_list") }}', dag=dag)
  start_step >> sort_list >> print_list