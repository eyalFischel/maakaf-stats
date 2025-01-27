FROM python:3.12.4

WORKDIR /discord

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-u",  "main.py"]