# HELPER FUNCTIONS
def send_message(client, channel_id, text):
    """Sends message of given text to a given channel_id from the given client."""

    client.chat_postMessage(channel=channel_id, text=text)


def get_dict_info(dictionary, info_to_get):
    """Returns list containing data from given dictionary."""

    return [dictionary.get(info) for info in info_to_get]
