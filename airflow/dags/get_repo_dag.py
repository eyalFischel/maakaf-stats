from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator
from datetime import datetime, timedelta
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("../scripts")

def run_script():
    from git_scripts.main import main
    main()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 28),  # Set the start date
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=15),
}


dag = DAG(
    'repository_data_collection_dag',
    default_args=default_args,
    description='A DAG to run repository data collection daily',
    schedule_interval=timedelta(days=1),  # Schedule to run once every day
    tags=["git"]
)

requirements = ["python-dotenv==0.21.0",
"requests==2.28.1",
"pydantic==1.10.2",
"psycopg2-binary==2.9.3",
"SQLAlchemy==2.0.30",
"logstash-formatter==0.5.17",
"python-json-logger==2.0.7"]

with dag:
    run_data_task = PythonVirtualenvOperator(
        task_id='run_repository_data_task',
        python_callable=run_script,
        requirements=requirements,
        system_site_packages=False,
        dag=dag
    )

