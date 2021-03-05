import json
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

default_args={
    'owner': 'airflow',
}


@dag(
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['example'],
)
def taskflow_etl():
    """
    #### Simple ETL Data Pipeline example
    """

    @task()
    def extract():
        """
        #### Extract task
        get data from source
        """

        data_string='{"1001":301.27,"1002":433.21,"2003":502.22}'
        order_data_dict = json.loads(data_string)
        return order_data_dict


    @task(multiple_outputs=True)
    def transform(order_data_dict: dict):
        """
        #### Transform Task
        Takes in the collection of order data and computes total
        """

        total_order_value = 0
        for value in order_data_dict.values():
            total_order_value += value

        return {"total_order_value": total_order_value}

    @task()
    def load(total_order_value: float):
        """
        ### Load task
        takes result from Transform and just prints it
        """
        print("Total order value is : %.2f"% total_order_value)

    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary['total_order_value'])


taskflow_etl_dag = taskflow_etl()





















