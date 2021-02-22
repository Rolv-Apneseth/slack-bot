import slack
import os
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter


# CONSTANTS
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(FILE_PATH, "assets")
ENV_PATH = os.path.join(ASSETS_PATH, ".env")

# SETUP
load_dotenv(dotenv_path=ENV_PATH)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app
)

client = slack.WebClient(token=os.environ["SLACK_API_TOKEN"])


if __name__ == "__main__":
    app.run(debug=True)
