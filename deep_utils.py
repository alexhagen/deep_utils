import inspect

def deep_hash(obj):
    """ deep_hash creates a hash from the object

    """
    objtree = tree(obj)
    return objtree.hash()

def deep_cmp(obj1, obj2):
    """ deep_cmp compares two objects deeply

    """
    obj1tree = tree(obj1)
    obj2tree = tree(obj2)
    return obj1tree.hash() == obj2tree.hash()

class tree(object):
    """ a tree is an object's structure
    """
    def __init__(self, obj):
        members = inspect.getmembers(obj)
        print members
        pass

    def string(self):
        """ returns the string representation of the object """

    def hash(self):
        """ returns the hash of the object and all its """
