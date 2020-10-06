from dataclasses import dataclass
import json

@dataclass
class Server:
    _id: int
    host_id: int
    host_name: int
    voice_id: int
    voice_name: str
    text_id: int
    text_name: str
    private: bool
    code: str
    region: str
    created: int
    finished: int
    current_players: []
    ban_players: []

    def to_json(self):
        return json.dumps(self.__dict__, default=lambda x: x.__dict__, indent=4)