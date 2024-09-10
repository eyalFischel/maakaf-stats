import logging
from pythonjsonlogger import jsonlogger

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the minimum level of messages to log

# Create a StreamHandler for console output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
console_handler.setFormatter(logging.Formatter(console_format))

# Create a FileHandler for JSON-formatted log output
file_handler = logging.FileHandler("github_data.log")
file_handler.setLevel(logging.DEBUG)
json_format = jsonlogger.JsonFormatter("%(asctime)s %(name)s %(levelname)s %(message)s")
file_handler.setFormatter(json_format)

# Add both handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
