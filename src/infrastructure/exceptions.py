class Exc(Exception):
    """
    Abstract exception class. Its instances are used on services'
    layer when something is wrong with user's request

    **Do not use it when there's an app problem, because `Exc`
    subclasses' instances are normally handled on API level**
    """
