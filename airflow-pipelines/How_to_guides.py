# Add tags to DAGs adn use it for filtering in the UI
from airflow import DAG

dag = DAG(
    dag_id = 'unique_dag_id',
    schedule_interval='0 0 * * *',
    tags=['example']
)

