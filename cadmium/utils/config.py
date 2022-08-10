"""Utilities for accessing and setting config parameters."""

import yaml

from cadmium.exceptions import *


class Config:
    def __init__(self):

        # Read config file
        with open("data/config.yml", "r") as file_:
            config = yaml.safe_load(file_) or {}

        self.channel = config.get("channel")
        self.color = config.get("color", 0x0000FF)
        self.interval = config.get("interval", "* * * * *")
        self.message = config.get("message", "The subject is")
        self.mention = config.get("mention", "")

        self.probs_verb = config.get("probs_verb", 0.5)
        self.probs_adverb = config.get("probs_adverb", 0.9)
        self.probs_adjective = config.get("probs_adjective", 0.8)
        self.probs_second_adjective = config.get("probs_second_adjective", 0.3)
        self.probs_verb_step = config.get("probs_verb_step", 0.2)

    def get(self, key):
        """Get config item."""

        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise InvalidConfigKeyError(f"Invalid configuration item: {key}")

    def set(self, key, value):
        """Set config item."""

        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise InvalidConfigKeyError(f"Invalid configuration item: {key}")

    def to_dict(self):
        """Get the configuration as a dict."""

        dict_ = {}

        for item in (
            "channel",
            "color",
            "interval",
            "message",
            "mention",
            "probs_verb",
            "probs_adverb",
            "probs_adjective",
            "probs_second_adjective",
            "probs_verb_step",
        ):
            dict_[item] = getattr(self, item)

        return dict_

    def write(self):
        """Write the configuration file."""

        with open("data/config.yml", "r") as file_:
            file_.write(self.to_dict())


_inst = Config()
get = _inst.get
set = _inst.set
to_dict = _inst.to_dict
