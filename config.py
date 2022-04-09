""" File that loads all the environment variables.
"""
from ast import literal_eval as lit_eval
from logging import getLogger
import os


logger = getLogger(__name__)


ENV = os.getenv('ENV', 'dev')
ENV_FILE = f'{ENV}.env'
if os.path.exists(ENV_FILE):
    from dotenv import find_dotenv, load_dotenv
    load_dotenv(find_dotenv(ENV_FILE))

#ORIGINS = lit_eval(os.getenv('ORIGINS', '[]'))
MONGO_URI = os.getenv('MONGO_URI')


errors = []
if not MONGO_URI:
    errors.append('MONGO_URI')

if errors:
    message = 'The next critical env vars are missing: \n'
    for e in errors:
        message += f'* {e}\n'
    logger.error(message)
    raise ValueError("Critical env vars missing.")
