<h1 align="center">
  <a href="https://maakaf.netlify.app">
    <picture>
      <img height="200" width="200" alt="maakaf" src="./docs/maakaf-logo.png">
    </picture>
  </a>
  <br>
  <a href="https://discord.gg/DBCM8EMXEC">
    <img src="https://img.shields.io/discord/704680098577514527?style=flat-square&label=%F0%9F%92%AC%20discord&color=00ACD7">
  </a>
</h1>
<p align="center">
  <em><b>maakaf-stats</b> is an open-source project that aims to collect and analyze data about the Maakaf community.</em>
</p>

---

## ⚠️ **Attention**

maakaf stats currently in beta and under active development. 
While it offers exciting new features, please note that it may not be stable for production use. 

---

## ⚙️ Installation

1. Install docker and docker-compose

2. Run the following commands in the root directory of the project:
```bash
docker compose up airflow-init
docker compose up 
```
* Wait a few seconds for the containers to finish starting
( you can include -d to run in detached mode)

3. Open the browser and go to the port depends on the service you want to use (grafana, airflow, etc.)

4. Enjoy!

* To kill the containers:
```bash
docker compose down
```

## 🎯 technologies

- [Airflow](https://airflow.apache.org/docs/apache-airflow/stable/index.html) - Being used to schedule and monitor the data collection process.
- [Grafana](https://grafana.com/docs/grafana/latest/)  - Being used to visualize the data collected.
- [Elasitcsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html) - Being used to store the logs.
- [Kibana](https://www.elastic.co/guide/en/kibana/current/index.html) - Being used to visualize the logs.
- [Docker](https://docs.docker.com/) - Being used to containerize the services.
- [Docker-compose](https://docs.docker.com/compose/) - Being used to manage the containers. 
- [Python](https://docs.python.org/3/) - Being used to write the data collection scripts.
- [Postgres](https://www.postgresql.org/docs/) - Being used to store the data.
- [FastAPI](https://fastapi.tiangolo.com/) - Being used to provide the data to other projects.

## 💡 Philosophy

Maakaf Stats aims to offer a straightforward and efficient way to collect and analyze data about our community. <br>
Our goal is to support the development and growth of both the community and its members.

## 🚀 Services
 - **Grafana**: To visualize the communitys stats. <TODO Update add domain or ip to login>
 - **API Service**: To provide the options to other projects to use the data collected by the service. <TODO Update add api docs>


## 👍 Contribute

If you want to say **Thank You** and/or support the active development of `maakaf-stats` feel free to add a [GitHub Star](https://github.com/eyalFischel/maakaf-stats/stargazers) to the project.

## 🖥️ Development

To ensure your contributions are ready for a Pull Request, please use the following `Makefile` commands. These tools help maintain code quality, consistency.

## 💻 Code Contributors

<a href="https://github.com/eyalFischel/maakaf-stats/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=eyalFischel/maakaf-stats" />
</a>

## 🧾 License

Copyright (c) 2024-present. Maakaf-stats is free and open-source software licensed under the [MIT License](https://github.com/eyalFischel/maakaf-stats/blob/main/LICENSE). 
