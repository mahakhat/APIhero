import openai
import logging.config
import json
from utils import config
from view import front

CONFIG_FILE = 'ressources/config.json'


def main():
    conf = config.load_config(CONFIG_FILE)
    openai.api_key = conf['API_KEY']
    with open(CONFIG_FILE, 'rt') as f:
        logger_json = json.load(f)
    logging.config.dictConfig(logger_json)
    front.run(conf)


if __name__ == "__main__":
    main()


