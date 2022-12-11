from datetime import datetime
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


# ==================================================
# DAG Definition

default_arguments = {
    'depends_on_past': False,
    'email': ['youremail@email.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    dag_id='penny_pipe',
    default_args = default_arguments,
    start_date= datetime(2022, 12, 8),
    schedule=timedelta(minutes=15)
)

    
project_filepath = '[YOUR PATH TO /penny/app]'  #Path to /penny/app, not just /penny
DBT_DIR = str(project_filepath) + '/dbt/penny'  #Generates directory for dbt models

extract = BashOperator(
    dag = dag,
    retries=1,
    task_id = 'extract',
    bash_command = f"""
    cd {project_filepath} &&
    source ./venv/bin/activate &&
    python3 extract.py
    """
)

build_model = BashOperator(
    dag = dag,
    retries=1,
    task_id = 'build_model',
    bash_command = f"""
    cd {DBT_DIR} &&
    dbt run
    """
)

extract >> build_model