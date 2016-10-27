import logging

logging.basicConfig(filename="snippets.log, level=logging.DEBUG")

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

    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name))

    return ""

