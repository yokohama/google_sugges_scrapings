import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

GOOGLE_API_JSON = os.environ.get("GOOGLE_API_JSON")
SPREAD_SHEET_KEY = os.environ.get("SPREAD_SHEET_KEY")
