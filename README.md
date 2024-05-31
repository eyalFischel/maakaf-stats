# maakaf-stats
A service to collect Maakaf's stats from Discord, LinkedIn, and Git for better understanding.

## How to run airflow
1. Install docker and docker-compose

2. Run
```bash
docker compose up airflow-init
docker compose up 
```
* Wait a few seconds for the containers to finish starting
( you can include -d to run in detached mode)

3. Open the browser and go to http://localhost:8080

4. Enjoy!

* user and password are `airflow`
* To kill the containers:
```bash
docker compose down
```