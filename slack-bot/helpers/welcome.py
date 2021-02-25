from helpers.message import Message


class WelcomeMessage(Message):
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

    def __init__(self, to_channel):
        super().__init__(to_channel)
        self.update_blocks()

    def update_blocks(self):
        """Sets blocks to be shown on message."""

        self.blocks = [self.START_TEXT, self.DIVIDER, self._get_reaction_task()]

    def _get_reaction_task(self):
        """Gets dictionary for reaction block of welcome message."""

        checkmark = ":white_check_mark:"
        if not self.is_completed:
            checkmark = ":white_large_square:"

        text = f"{checkmark} *React to this message!*"

        return {"type": "section", "text": {"type": "mrkdwn", "text": text}}
