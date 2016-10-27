import argparse
import logging

logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """
    Store a snippet with an associated name
    :param name: name of snippet
    :param snippet: snippet detail
    :return: name and the snippet
    """

    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))

    return name, snippet


def get(name):
    """
    Retrieve snippet with a given name
    :param name: name of snippet to retrieve
    :return: snippet
    """

    logging.error("FIXME: Unimplemented - put({!r})".format(name))

    return ""


def main():
    """
    Main Function
    """
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="name of the snippet")
    put_parser.add_argument("snippet", help="snippet text")

    arguments = parser.parse_args()


if __name__ == "__main__":
    main()
