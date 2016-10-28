import argparse
import logging
import psycopg2

logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established")


def put(name, snippet):
    """
    Store a snippet with an associated name
    :param name: name of snippet
    :param snippet: snippet detail
    :return: name and the snippet
    """

    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    command = "insert into snippets values (%s, %s)"
    cursor.execute(command, (name, snippet))
    connection.commit()
    logging.debug("Snippet stored succesfully.")

    return name, snippet


def get(name):
    """
    Retrieve snippet with a given name
    :param name: name of snippet to retrieve
    :return: snippet or not found message
    """

    logging.info("Retrieving snippet {!r}".format(name))
    cursor = connection.cursor()
    command = "select * from snippets where keyword = (%s)"
    cursor.execute(command, (name,))
    result = cursor.fetchone()
    connection.commit()

    if not result:
        return "404: Snippet not found"

    return result[0]


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

    logging.debug("Constructing a get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="name of the snippet to retrieve")

    arguments = parser.parse_args()

    #convert the Namespace object to a dictionary
    arguments = vars(arguments)

    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))


if __name__ == "__main__":
    main()
