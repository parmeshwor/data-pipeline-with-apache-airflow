import json

from airflow import DAG

from airflow.operators.python import PythonOperator
from airflow.utils.dates import  days_ago

default_args={
    'owner': 'airflow',
}

with DAG(
    'taskflow_etl_v1',
    default_args= default_args,
    description='ETL DAG',
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['example'],
) as dag:
    dag.doc_md = __doc__

    def extract(**kwargs):
        ti = kwargs['ti']
        data_string='{"1001":301.27,"1002":433.21,"1003":502.22}'
        ti.xcom_push('order_data', data_string)

    def transform(**kwargs):
        ti = kwargs['ti']
        extract_data_string= ti.xcom_pull(task_ids='extract', key='order_data')
        order_data = json.loads(extract_data_string)

        total_order_value = 0
        for value in order_data.values():
            total_order_value += value

        total_value = {'total_order_value': total_order_value}
        total_value_json_string = json.dumps(total_value)
        ti.xcom_push('total_order_value',total_value_json_string)

    def load(**kwargs):

        ti = kwargs['ti']
        total_value_string = ti.xcom_pull(task_ids='transform',key='total_order_value')
        total_order_value = json.loads(total_value_string)

        print(total_order_value)

    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )

    extract_task.doc_md = """
    #### Extract task
    A simple extract task to get data for pipeline
    """

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )

    transform_task.doc_md = """
    #### Load Task
    Takes result from xcom and computes the sum and put back to xcom
    """

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
    )

    load_task.doc_md = """
    #### Load task
    pull data from xcom and print it out
    """

    extract_task >> transform_task >> load_task


































































