from datetime import timedelta
from airflow import DAG  # The DAG object; we need to instantiate a DAG
from airflow.operators.bash import BashOperator  # operators
from airflow.utils.dates import days_ago

# below args will get passed on to each operator
# you can override them on a per-task basis during operator initialization

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'basic_pipeline',
    default_args=default_args,
    description='A simple dag',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['example']
)

# t1 and t2 are examples of tasks created by instantiating operators

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)


t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    retries=3,
    dag=dag
)

dag.doc_md = __doc__

t1.doc_md = """
#### Task Documentation
You can document your task using the attributes 'doc_md' (markdown)
"""

templated_command ="""
{% for i in range(5) %}
    echo "{{ ds }}"
    echo "{{ macros.ds_add(ds,7) }}"
    echo "{{ params.my_param }}"
{% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    depends_on_past=False,
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in '},
    dag=dag,
)

t1 >> [t2,t3]