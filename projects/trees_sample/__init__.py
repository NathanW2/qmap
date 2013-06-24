import getpass

def onProjectLoad():
    """
        Return false if project shouldn't be loaded, else return True.
    """
    user = getpass.getuser()
    return user == "nathan.woodrow2"

def ProjectLoaded():
    pass