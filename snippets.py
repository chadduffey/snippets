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

    with connection, connection.cursor() as cursor:
        try:
            cursor.execute("insert into snippets values (%s, %s)", (name, snippet))
        except:
            connection.rollback()
            cursor.execute("update snippets set message=%s where keyword=%s", (snippet, name))
        connection.commit()

    logging.debug("Snippet stored successfully.")

    return name, snippet


def get(name):
    """
    Retrieve snippet with a given name
    :param name: name of snippet to retrieve
    :return: snippet or not found message
    """

    logging.info("Retrieving snippet {!r}".format(name))

    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        result = cursor.fetchone()

    if not result:
        return "404: Snippet not found"

    logging.info("Retrieved snippet {!r}".format(name))

    return result[0]


def catalog():
    """
    See all of the current snippets
    :return: all of the current inventory in a tuple
    """
    logging.info("Retrieving the entire catalog")

    with connection, connection.cursor() as cursor:
        cursor.execute("select * from snippets")
        result = cursor.fetchall()

    if not result:
        return False

    logging.info("Retrieved the entire catalog")

    return result


def search(value):
    """
    Find snippets containing the search value
    :param value: the value to search for in the database
    :return: items matching the search criteria in a tuple
    """
    logging.info("Searching for {!r}".format(value))

    with connection, connection.cursor() as cursor:
        query = "SELECT * FROM snippets WHERE message LIKE '%" + value + "%'"
        cursor.execute(query)
        result = cursor.fetchall()

    if not result:
        return False

    return result


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

    logging.debug("Constructing a catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Retrieve all snippets")

    logging.debug("Constructing a search subparser")
    search_parser = subparsers.add_parser("search", help="Find snippets with keyword")
    search_parser.add_argument("value", help="string of the snippet to find")

    arguments = parser.parse_args()

    # convert the Namespace object to a dictionary
    arguments = vars(arguments)

    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command == "catalog":
        all_items = catalog()
        if all_items:
            for k, v in all_items:
                print(k + '\t[' + v + ']')
    elif command == "search":
        snippets = search(**arguments)
        if snippets:
            for k,v in snippets:
                print(k + '\t[' + v + ']')


if __name__ == "__main__":
    main()
