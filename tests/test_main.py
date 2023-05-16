from unittest.mock import patch

from exceptions import TrelloException
from main import main


@patch("main.Parser")
@patch("main.TrelloConfig")
@patch("main.TrelloFetcher")
@patch("main.sys")
def test_main_success(mock_sys, mock_fetcher, *_):
    cards = [{"id": 1}]
    mock_fetcher.return_value.get_cards_with_selected_field.return_value = cards
    main()
    mock_sys.stdout.write.assert_called_once_with('{"id": 1}\n')


@patch("main.Parser")
@patch("main.TrelloConfig")
@patch("main.TrelloFetcher")
@patch("main.sys")
def test_main_failed_trello_except(mock_sys, mock_fetcher, *_):
    mock_fetcher.return_value.get_cards_with_selected_field.side_effect = TrelloException(
        "error", 2
    )
    main()
    mock_sys.stderr.write.assert_called_once_with("error")
    mock_sys.exit.assert_called_once_with(2)


@patch("main.Parser")
@patch("main.TrelloConfig")
@patch("main.TrelloFetcher")
@patch("main.sys")
def test_main_failed_main_except(mock_sys, mock_fetcher, *_):
    mock_fetcher.return_value.get_cards_with_selected_field.side_effect = KeyError("error")
    main()
    mock_sys.stderr.write.assert_called_once_with("'error'")
    mock_sys.exit.assert_called_once_with(1)
