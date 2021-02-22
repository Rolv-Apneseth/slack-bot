import slack
import os
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter


# CONSTANTS
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(FILE_PATH, "assets")
ENV_PATH = os.path.join(ASSETS_PATH, ".env")
USEFUL_EVENT_INFO = ["channel", "user", "text"]

# SETUP
load_dotenv(dotenv_path=ENV_PATH)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app
)

client = slack.WebClient(token=os.environ["SLACK_API_TOKEN"])

BOT_USER_ID = client.api_call("auth.test")["user_id"]


# HELPER FUNCTIONS
def send_message(client, channel_id, text):
    """Sends message of given text to a given channel_id from the given client."""

    client.chat_postMessage(channel=channel_id, text=text)


def get_event_info(event, info_to_get):
    """Returns list containing data from given event object."""

    return [event.get(info) for info in info_to_get]


# EVENT HANDLER FUNCTIONS
@slack_event_adapter.on("message")
def on_message(payload):
    event = payload.get("event", {})
    channel_id, user_id, text = get_event_info(event, USEFUL_EVENT_INFO)


if __name__ == "__main__":
    app.run(debug=True)
