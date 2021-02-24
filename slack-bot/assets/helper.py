from assets import welcome


# HELPER FUNCTIONS
def send_message(client, channel_id, text):
    """
    Sends message of given text to a given channel_id.

    To make a message a direct message to a user you can
    simply put '@' in front of the user id, i.e. use
    `f'@{user_id}'` in place of channel_id.
    """

    client.chat_postMessage(channel=channel_id, text=text)


def get_dict_info(dictionary, info_to_get):
    """Returns list containing data from given dictionary."""

    return [dictionary.get(info) for info in info_to_get]


def send_welcome_message(client, channel_id, user_id):
    """
    Sends welcome message to a given channel.

    Returns a WelcomeMessage object.
    """
    welcome_message = welcome.WelcomeMessage(channel_id, user_id)
    message = welcome_message.get_message()
    response = client.chat_postMessage(**message)
    welcome_message.timestamp = response["ts"]

    return welcome_message
