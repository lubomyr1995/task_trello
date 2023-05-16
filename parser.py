import argparse


class Parser:
    @staticmethod
    def parse_arguments() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Fetch cards from Trello API")
        parser.add_argument("config_path", help="Path to config file")
        return parser.parse_args()
