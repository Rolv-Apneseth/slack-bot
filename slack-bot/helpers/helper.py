from datetime import datetime, timedelta

from helpers import welcome


# HELPER FUNCTIONS
def send_message(client, channel_id, text):
    """
    Sends message of given text to a given channel_id.

    To make a message a direct message to a user you can
    simply put '@' in front of the user id, i.e. use
    `f'@{user_id}'` in place of channel_id.
    """

    client.chat_postMessage(channel=channel_id, text=text)


def reply_message(client, channel_id, ts, text):
    """Replies to a message on the given channel_id in a thread."""

    client.chat_postMessage(
        channel=channel_id,
        thread_ts=ts,
        text=text,
    )


def get_timestamp(seconds=0, minutes=0, hours=0, days=0):
    """
    Returns a timestamp for a given time in the future provided in keyword arguments.
    """
    MINIMUM = timedelta(seconds=14)
    delta = timedelta(seconds=0, minutes=0, hours=0, days=0)
    delta = delta if delta > MINIMUM else MINIMUM

    return (datetime.now() + delta).timestamp()


def schedule_message(client, channel, text, ts):
    """Schedule a message to be posted to the given channel."""

    client.chat_scheduleMessage(channel=channel, text=text, post_at=ts)


def get_dict_info(dictionary, info_to_get):
    """Returns list containing data from given dictionary."""

    return [dictionary.get(info) for info in info_to_get]


def send_welcome_message(client, channel_id):
    """
    Sends welcome message to a given channel.

    Returns a WelcomeMessage object.
    """
    welcome_message = welcome.WelcomeMessage(channel_id)
    message = welcome_message.get_message()
    response = client.chat_postMessage(**message)
    welcome_message.timestamp = response["ts"]

    return welcome_message


def verify_number(string):
    """Returns a boolean value on whether a given string is a positive integer."""

    try:
        integer = int(string)
        assert integer > 0
    except (ValueError, AssertionError):
        return False
    return True
