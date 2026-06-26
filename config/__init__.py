import os
import yaml
from dotenv import load_dotenv
from logging.config import dictConfig

load_dotenv()

HOSTNAME = os.environ.get("HOSTNAME", "0.0.0.0")
PORT = os.environ.get("PORT", "8888")

logger_config_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'logger.yml'))
with open(logger_config_path, 'r') as stream:
    logger_config = yaml.load(stream, Loader=yaml.FullLoader)
    dictConfig(logger_config)
