import json

from exceptions import TrelloException


class TrelloConfig:
    def __init__(self, config_path: str) -> None:
        self._config_path = config_path
        self.config = self.read_config()

    def read_config(self) -> dict:
        try:
            with open(self._config_path) as file:
                config = json.load(file)
            return config
        except FileNotFoundError:
            msg = f"File {self._config_path} not found"
            raise TrelloException(msg, 1)
        except json.JSONDecodeError:
            msg = f"File {self._config_path} not valid JSON"
            raise TrelloException(msg, 1)

    def _get_field(self, field: str) -> str:
        try:
            config = self.config
            for key in field.split("."):
                config = config[key]
            return config
        except KeyError:
            msg = f"Missing field {field} in {self._config_path}"
            raise TrelloException(msg, 1)

    @property
    def access_token(self) -> str:
        return self._get_field("credential.access_token")

    @property
    def api_key(self) -> str:
        return self._get_field("credential.api_key")

    @property
    def board_id(self) -> str:
        return self._get_field("boardId")
