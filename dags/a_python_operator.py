import time
from pprint import pprint
from airflow import DAG

from airflow.operators.python import PythonOperator, PythonVirtualenvOperator
from airflow.utils.dates import days_ago

args = {
    'owner':'airflow',
}

dag = DAG(
    dag_id="a_python_operator",
    default_args=args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['example'],
)


# [ START howto operator python ]

def print_context(ds, **kwargs):
    """
    print the Airflow context and ds variable from the context
    :param ds:
    :param kwargs:
    :return:
    """
    pprint(kwargs)
    print(ds)
    return "Whenever you return gets printed in the logs"


run_this = PythonOperator(
    task_id='print_the_context',
    python_callable=print_context,
    dag=dag,
)

# [End howto operator python]


def my_sleeping_function(random_base):
    """This is a function that will run within the DAG execution """
    time.sleep(random_base)


# Generate 5 sleeping tasks, sleeping from 0.0 to 0.4 seconds respectively

for i in range(5):
    task = PythonOperator(
        task_id='sleep_for_'+str(i),
        python_callable=my_sleeping_function,
        op_kwargs={'random_base':float(i)/10},
        dag=dag,
    )