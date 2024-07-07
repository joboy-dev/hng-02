import os
from secrets import token_hex
from typing import List, Optional
from dotenv import load_dotenv
from pathlib import Path

def generate_id() -> str:
    '''Returns a random string identifier for database models'''

    return token_hex(16)


def get_env_value(key):
    '''Returns the value of an environment variable'''

    BASE_DIR = Path(__file__).resolve().parent.parent

    load_dotenv(os.path.join(BASE_DIR, '.env'))
    return os.getenv(key)


def convert_model_to_dict(model, fields_to_remove: Optional[List[str]] = None):
    '''Returns a dictionary version of a model'''

    dictionary = {column.name: getattr(model, column.name) for column in model.__table__.columns}

    if fields_to_remove:
        for field in fields_to_remove:
            dictionary.pop(field)
    
    return dictionary