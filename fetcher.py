import requests

from config import TrelloConfig
from exceptions import TrelloException


class TrelloFetcher:
    base_url = "https://api.trello.com/1"

    def __init__(self, config: TrelloConfig) -> None:
        self.config = config

    def get_board_cards(self) -> list[dict]:
        response = requests.get(self.url_for_get_cards, params=self.params_for_auth)

        if not response.ok:
            raise TrelloException(response.text, 2)
        return response.json()

    def get_cards_with_selected_field(self) -> list:
        cards = self.get_board_cards()
        try:
            selected_cards = []
            for card in cards:
                output = {
                    "id": card["id"],
                    "name": card["name"],
                    "description": card["desc"],
                    "url": card["url"],
                    "list": card["idList"],
                    "labels": card["labels"],
                    "members": card["idMembers"],
                }
                selected_cards.append(output)
            return selected_cards
        except KeyError as err:
            msg = f"API missing field {str(err)}"
            raise TrelloException(msg, 2)

    @property
    def params_for_auth(self) -> dict[str, str]:
        return {"key": self.config.api_key, "token": self.config.access_token}

    @property
    def url_for_get_cards(self) -> str:
        return f"{self.base_url}/boards/{self.config.board_id}/cards"
