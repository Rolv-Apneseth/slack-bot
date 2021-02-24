class WelcomeMessage:
    START_TEXT = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Welcome to this channel\n\n" "*Get started by completing the tasks*"
            ),
        },
    }

    DIVIDER = {"type": "divider"}

    def __init__(self, channel, user_id):
        self.channel = channel
        self.user_id = user_id
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.is_completed = False

    def get_message(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "blocks": [self.START_TEXT, self.DIVIDER, self._get_reaction_task()],
        }

    def _get_reaction_task(self):
        checkmark = ":white_check_mark:"
        if not self.is_completed:
            checkmark = ":white_large_square:"

        text = f"{checkmark} *React to this message!*"

        return {"type": "section", "text": {"type": "mrkdwn", "text": text}}
