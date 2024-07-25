import os

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

"""
This DAG runs a simple bash command
"""

# dir
scripts_path = os.path.dirname(__file__)
scripts_path = scripts_path.replace("dags", "scripts")
script_path = os.path.join(scripts_path, "example/example.py")

default_args = {
    "owner": "airflow",  # Owner of the DAG
    "depends_on_past": False,  # Don't depend on past runs
    "start_date": datetime(2024, 5, 30),  # Start date of the DAG
    "email_on_failure": False,  # Don't email on failure
    "email_on_retry": False,  # Don't email on retry
    "retries": 0,  # Number of retries
    "retry_delay": timedelta(minutes=5),  # How long to wait before retrying
}

dag = DAG(
    "example",  # DAG ID
    default_args=default_args,  # Specified above
    catchup=False,  # Perform tasks that haven't run
    max_active_runs=1,  # Run at most one DAG at a time
    schedule_interval="0 19 * * *",
)  # Run daily at midnight

task = BashOperator(
    task_id="example_task_script",  # Task ID
    bash_command=f"python3 {script_path}",  # Command to run
    dag=dag,  # Reference to the DAG
)
