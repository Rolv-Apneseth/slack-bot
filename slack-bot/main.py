import slack
import os
from dotenv import load_dotenv

# CONSTANTS
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(FILE_PATH, 'assets')
ENV_PATH = os.path.join(ASSETS_PATH, '.env')

# SETUP
load_dotenv(dotenv_path=ENV_PATH)

client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
