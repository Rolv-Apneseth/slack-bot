class Message:
    def __init__(self, to_channel):
        self.to_channel = to_channel
        self.timestamp = ""
        self.text = ""
        self.blocks = []

        self.is_completed = False

    def get_message(self):
        return {
            "ts": self.timestamp,
            "channel": self.to_channel,
            "text": self.text,
            "blocks": self.blocks,
        }
