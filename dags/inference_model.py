import json
import os
from airflow import DAG
from airflow.models import Variable
import airflow
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "data-axle",
    "start_date": airflow.utils.dates.days_ago(2),
    "depends_on_past": False,
    'email': ['airflow@example.com'],
    "current_path": os.path.abspath(os.path.dirname(__file__)),
    "retries": 0,
}

config_file = default_args['current_path'] + '/config.json'
with open(config_file) as f:
    config = json.load(f)

with DAG(
    "airflow-databricks-inference",
    default_args=default_args,
    description="submit databricks job for model inferencing",
    schedule_interval="@once",
    max_active_runs=1,
    is_paused_upon_creation=True
) as dag:
    new_cluster = {
        # TODO replace with commented code
        'spark_version': '2.1.0-db3-scala2.11', # config["spark_version"],
        'node_type_id': 'r3.xlarge', # config["node_type_id"],
        'aws_attributes': {'availability': 'ON_DEMAND'},
        'num_workers': 8, # config["num_workers"],
    }

    notebook_task_params = {
        'new_cluster': new_cluster,
        'notebook_task': {
            'notebook_path': '/Users/prarwork@gmail.com/PrepareData',
        },
    }

def check_default(key: str, default):
    if key in config:
        return config[key]
    else:
        return default

def get_extra_py_files(key):
    if key in config:
        return {"--extra-py-files": config[key]}
    else:
        return {}

start_process = DummyOperator(task_id="Begin_Execution", dag=dag)
end_process = DummyOperator(task_id="Stop_Execution", dag=dag)

submit_databricks_job = DatabricksSubmitRunOperator(
    task_id='spark_jar_task',
    new_cluster=new_cluster,
    spark_jar_task={'main_class_name': 'ProcessData'},
    # libraries=[{'jar': 'dbfs:/lib/etl-0.1.jar'}],
)

start_process >> submit_databricks_job >> end_process
