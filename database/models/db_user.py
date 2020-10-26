from dataclasses import dataclass
import json

@dataclass
class User:
    player_id: int
    like: int
    dislike: int
    badge: []

    def to_json(self):
        return json.dumps(self.__dict__, default=lambda x: x.__dict__, indent=4)