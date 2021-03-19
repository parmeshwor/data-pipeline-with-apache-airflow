"""DAG demonstrating usage of bash operator"""

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from datetime import timedelta


"""
task_runtime_id_1  --\
task_runtime_id_2  ---->  run_this_after_loop ---> run_this_last
task_runtime_id_3 --/

also_run_this --> run_this_last

"""
args ={
    'owner': 'airflow',
}


dag = DAG(
    dag_id='a_bash_operator',
    default_args=args,
    start_date=days_ago(1),
    schedule_interval='0 0 * * *',
    tags=['example','example2'],
    dagrun_timeout=timedelta(minutes=60),
    params={"example_key": "example_value"},

)

run_this_last = DummyOperator(
    task_id='run_this_last',
    dag=dag,
)

run_this_after_loop = BashOperator(
    task_id='run_this_after_loop',
    bash_command='echo 1',
    dag=dag
)

run_this_after_loop>>run_this_last


for i in range(3):
    task_runme_id = BashOperator(
        task_id='runme_' + str(i),
        bash_command='echo "{{ task_instance_key_str }}" && sleep 1',
        dag=dag,
    )
    task_runme_id>>run_this_after_loop

# bash template
also_run_this = BashOperator(
    task_id='also_run_this',
    bash_command='echo "run_id={{run_id}} | dag_run={{ dag_run}}"',

)

also_run_this >> run_this_last

if __name__=='__main__':
    dag.cli()



