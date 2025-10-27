import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
env_path = BASE_DIR / '.env'
load_dotenv(env_path)

def get_env_variable(var_name, default=None):
    """Get environment variable or return default value"""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        error_msg = f'Set the {var_name} environment variable'
        raise Exception(error_msg)