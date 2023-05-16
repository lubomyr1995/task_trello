from unittest.mock import Mock, patch

import pytest

from exceptions import TrelloException
from fetcher import TrelloFetcher

MOCKED_CONFIG = Mock(access_token="test_token", api_key="test_key", board_id="test_id")


def test_params_for_auth():
    fetcher = TrelloFetcher(MOCKED_CONFIG)
    assert fetcher.params_for_auth == {"key": "test_key", "token": "test_token"}


def test_url_for_get_cards():
    fetcher = TrelloFetcher(MOCKED_CONFIG)
    assert fetcher.url_for_get_cards == f"{fetcher.base_url}/boards/test_id/cards"


@patch("fetcher.requests")
def test_get_board_cards_success(mock_requests):
    response = Mock(ok=True)
    response.json.return_value = []

    mock_requests.get.return_value = response
    fetcher = TrelloFetcher(MOCKED_CONFIG)
    cards = fetcher.get_board_cards()
    assert cards == []


@patch("fetcher.requests")
def test_get_board_cards_failed(mock_requests):
    response = Mock(ok=False)
    response.text = "error"

    mock_requests.get.return_value = response
    fetcher = TrelloFetcher(MOCKED_CONFIG)
    with pytest.raises(TrelloException) as exc_info:
        fetcher.get_board_cards()

    assert exc_info.value.msg == "error"
    assert exc_info.value.status_code == 2


@patch("fetcher.requests")
def test_get_cards_with_selected_field_success(mock_requests):
    response = Mock(ok=True)
    response.json.return_value = [
        {
            "id": 1,
            "name": "first_card",
            "desc": "",
            "url": "",
            "idList": "",
            "labels": [],
            "idMembers": [],
            "ids": 1,
        }
    ]

    mock_requests.get.return_value = response
    fetcher = TrelloFetcher(MOCKED_CONFIG)
    cards = fetcher.get_cards_with_selected_field()
    assert cards == [
        {
            "id": 1,
            "name": "first_card",
            "description": "",
            "url": "",
            "list": "",
            "labels": [],
            "members": [],
        }
    ]


@patch("fetcher.requests")
def test_get_cards_with_selected_field_failed(mock_requests):
    response = Mock(ok=True)
    response.json.return_value = [
        {
            "id": 1,
            "name": "first_card",
            "desc": "",
            "url": "",
            "idLis": "",
            "labels": [],
            "idMembers": [],
        }
    ]

    mock_requests.get.return_value = response
    fetcher = TrelloFetcher(MOCKED_CONFIG)
    with pytest.raises(TrelloException) as exc_info:
        _ = fetcher.get_cards_with_selected_field()

    assert exc_info.value.msg == f"API missing field 'idList'"
    assert exc_info.value.status_code == 2
