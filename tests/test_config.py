import json
import pytest

from config import TrelloConfig
from exceptions import TrelloException

SUCCESS_CONFIG = {
    "credential": {
        "access_token": "2bafb2d37185755693a2e64c5c54569E6B22891",
        "api_key": "ee1fa4852",
    },
    "boardId": "cc432046",
}
UN_SUCCESS_CONFIG = {
    "credential": {
        "access_tokes": "2bafb2d37185755693a2e64c5c54569E6B22891",
        "api_keys": "ee1fa4852",
    },
    "boardIds": "cc432046",
}


def test_read_config_success(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(SUCCESS_CONFIG))
    config = TrelloConfig(str(config_path))
    data = config.read_config()
    assert data == SUCCESS_CONFIG


def test_read_config_not_found(tmp_path):
    not_found_path = tmp_path / "conf.json"

    with pytest.raises(TrelloException) as exc_info:
        TrelloConfig(str(not_found_path)).read_config()
    assert exc_info.value.msg == f"File {not_found_path} not found"
    assert exc_info.value.status_code == 1


def test_read_config_invalid_json(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text("{")

    with pytest.raises(TrelloException) as exc_info:
        TrelloConfig(str(config_path)).read_config()
    assert exc_info.value.msg == f"File {config_path} not valid JSON"
    assert exc_info.value.status_code == 1


def test_access_token_success(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(SUCCESS_CONFIG))
    access_token = TrelloConfig(str(config_path)).access_token
    assert access_token == SUCCESS_CONFIG["credential"]["access_token"]


def test_access_token_key_error(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(UN_SUCCESS_CONFIG))
    with pytest.raises(TrelloException) as exc_info:
        _ = TrelloConfig(str(config_path)).access_token

    assert (
        exc_info.value.msg == f"Missing field credential.access_token in {config_path}"
    )
    assert exc_info.value.status_code == 1


def test_api_key_success(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(SUCCESS_CONFIG))
    api_key = TrelloConfig(str(config_path)).api_key
    assert api_key == SUCCESS_CONFIG["credential"]["api_key"]


def test_api_key_error(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(UN_SUCCESS_CONFIG))
    with pytest.raises(TrelloException) as exc_info:
        _ = TrelloConfig(str(config_path)).api_key
    assert exc_info.value.msg == f"Missing field credential.api_key in {config_path}"
    assert exc_info.value.status_code == 1


def test_board_id_success(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(SUCCESS_CONFIG))
    board_id = TrelloConfig(str(config_path)).board_id
    assert board_id == SUCCESS_CONFIG["boardId"]


def test_board_id_error(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(UN_SUCCESS_CONFIG))
    with pytest.raises(TrelloException) as exc_info:
        _ = TrelloConfig(str(config_path)).board_id
    assert exc_info.value.msg == f"Missing field boardId in {config_path}"
    assert exc_info.value.status_code == 1
