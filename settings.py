import os

from dotenv import load_dotenv

env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "secret.env")
load_dotenv(env_file)  # take environment variables from .env.

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
