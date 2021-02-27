import slack
import os
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import profanity_check

from helpers import helper

# CONSTANTS
FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(FOLDER_PATH, ".env")

USEFUL_EVENT_INFO = ["channel", "user", "text", "ts"]
EVENTS_PATH = "/slack/events"
COMMANDS_ROUTES = {
    "messages_count": "/messages-count",
    "reminder_mins": "/reminder-mins",
}

PROFANITY_RESPONSE = "Please do not include profanity in your messages!"

# SETUP
load_dotenv(dotenv_path=ENV_PATH)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ["SLACK_SIGNING_SECRET"], EVENTS_PATH, app
)

client = slack.WebClient(token=os.environ["SLACK_API_TOKEN"])

BOT_USER_ID = client.api_call("auth.test")["user_id"]
messages_counter = {}
welcome_messages = {}


# EVENT HANDLER FUNCTIONS
@slack_event_adapter.on("message")
def on_message(payload):
    # Get basic info
    event = payload.get("event", {})
    channel_id, user_id, text, ts = helper.get_dict_info(event, USEFUL_EVENT_INFO)

    # Stop function if user is a bot or if no user is provided (i.e. on message update)
    if not user_id or user_id == BOT_USER_ID:
        return

    # Increase messages counter for this user
    if user_id in messages_counter:
        messages_counter[user_id] += 1
    else:
        messages_counter[user_id] = 1

    # Start message
    if text.lower() == "start" and f"@{user_id}" not in welcome_messages:
        welcome_message = helper.send_welcome_message(client, f"@{user_id}")
        welcome_messages[f"@{user_id}"] = welcome_message
    # Profanity response
    elif profanity_check.predict([text.lower()])[0]:
        helper.reply_message(client, channel_id, ts, PROFANITY_RESPONSE)


@slack_event_adapter.on("reaction_added")
def on_reaction(payload):
    event = payload.get("event", {})
    reacted_item = event.get("item", {})
    channel_id = reacted_item.get("channel")
    user_id = event.get("user")

    if f"@{user_id}" not in welcome_messages:
        return

    welcome_message = welcome_messages[f"@{user_id}"]
    welcome_message.is_completed = True
    welcome_message.update_blocks()
    welcome_message.to_channel = channel_id
    welcome_messages[channel_id] = welcome_messages[f"@{user_id}"]
    del welcome_messages[f"@{user_id}"]

    message = welcome_message.get_message()
    response = client.chat_update(**message)
    welcome_message.timestamp = response["ts"]


# COMMAND FUNCTIONS
@app.route(COMMANDS_ROUTES["messages_count"], methods=["POST"])
def messages_count():
    form_data = request.form
    user_id, channel_id = helper.get_dict_info(form_data, ["user_id", "channel_id"])

    helper.send_message(
        client,
        channel_id,
        f"User {user_id} has sent {messages_counter.get(user_id, 0)} messages",
    )

    return Response(), 200


@app.route(COMMANDS_ROUTES["reminder_mins"], methods=["POST"])
def reminder_minutes():
    form_data = request.form
    user_id, text = helper.get_dict_info(form_data, ["user_id", "text"])
    dm_channel = f"@{user_id}"

    if helper.verify_number(text):
        helper.schedule_message(
            client,
            dm_channel,
            f"{text} minute(s) have passed!",
            helper.get_timestamp(minutes=int(text)),
        )
        helper.send_message(client, dm_channel, f"Reminder set for {text} minute(s)")
    else:
        helper.send_message(
            client,
            dm_channel,
            (
                "Your command failed to load. "
                "Please provide a positive whole number for the minutes argument. "
                f"Argument you provided: '{text}'"
            ),
        )

    return Response(), 200


if __name__ == "__main__":
    app.run(debug=True)
