import logging

from pythonjsonlogger import jsonlogger

Logger = logging.getLogger("discord_bot")
Logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("discord_logs.jsonl")
json_formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s"
)

file_handler.setFormatter(json_formatter)

Logger.addHandler(file_handler)
