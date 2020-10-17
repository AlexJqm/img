from dataclasses import dataclass
import json

@dataclass
class Server:
    _id: int
    host_id: int
    voice_id: int
    text_id: int
    private: bool
    code: str
    region: str

    def to_json(self):
        return json.dumps(self.__dict__, default=lambda x: x.__dict__, indent=4)