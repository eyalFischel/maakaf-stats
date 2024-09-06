FROM python:3.12.4

WORKDIR /discord_bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-u",  "discord_bot.py"]