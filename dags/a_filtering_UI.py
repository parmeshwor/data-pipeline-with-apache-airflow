from airflow import DAG


dag = DAG(
    dag_id='a_filtering_UI',
    schedule_interval="0 0 * * *",
    tags=['example', 'filter', 'ui']
)


