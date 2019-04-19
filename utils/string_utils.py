def get_sent_from_string(contents, sep=None):
    """

    :param contents:
    :param sep:
    :return:
    """
    if sep is not None:
        sentences = contents.split(sep)
    else:
        sentences = contents.split()
    return sentences


def string2list(string):
    """

    :param string:
    :return:
    """
    return [char for char in string]


def strip_string(string):
    """

    :param string:
    :return:
    """
    return string.strip()
