def get_page(start: int, size: int) -> int:
    """
    Counts page of a list of items

    :param start: start index of page(object is included into list)
    :param size: size of page
    :return int: page number
    """

    return start // size + 1 if start >= size else int(start != 1) + 1


def get_has_previous(start: int) -> bool:
    """
    Finds if there's a previous page

    :param start: start index of page(object is included into list)
    :return bool: existance of previous page
    """

    return start > 1


def get_has_next(total: int, start: int, size: int) -> bool:
    """
    Finds if there's a next page

    :param total: total amount of objects in storage
    :param start: start index of page(object is included into list)
    :param size: size of page
    :return bool: existance of next page
    """

    return start + size < total
