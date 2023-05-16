import json
import sys

from config import TrelloConfig
from exceptions import TrelloException
from fetcher import TrelloFetcher
from parser import Parser


def main() -> None:
    try:
        args = Parser.parse_arguments()
        config = TrelloConfig(args.config_path)
        cards = TrelloFetcher(config).get_cards_with_selected_field()
        for card in cards:
            sys.stdout.write(f"{json.dumps(card)}\n")
    except TrelloException as err:
        sys.stderr.write(err.msg)
        sys.exit(err.status_code)
    except Exception as err:
        sys.stderr.write(str(err))
        sys.exit(1)


if __name__ == "__main__":
    main()
