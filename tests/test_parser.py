import argparse

from parser import Parser


def test_parse_arguments_for_get_cards():
    args = Parser.parse_arguments()
    assert isinstance(args, argparse.Namespace)
    assert args.config_path is not None
