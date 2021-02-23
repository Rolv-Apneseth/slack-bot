import slack
import os
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

from assets import welcome, helper

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
messages_counter = {}


# EVENT HANDLER FUNCTIONS
@slack_event_adapter.on("message")
def on_message(payload):
    event = payload.get("event", {})
    channel_id, user_id, text = helper.get_dict_info(event, USEFUL_EVENT_INFO)

    if not user_id or user_id == BOT_USER_ID:
        return None

    # Increase messages counter for this user
    if user_id in messages_counter:
        messages_counter[user_id] += 1
    else:
        messages_counter[user_id] = 1


# COMMAND FUNCTIONS
@app.route("/messages-count", methods=["POST"])
def messages_count():
    form_data = request.form
    user_id, channel_id = helper.get_dict_info(form_data, ["user_id", "channel_id"])

    helper.send_message(
        client,
        channel_id,
        f"User {user_id} has sent {messages_counter.get(user_id, 0)} messages",
    )

    return Response(), 200


if __name__ == "__main__":
    app.run(debug=True)
