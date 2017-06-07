import inspect
import hashlib
import weakref
import re
import sys
import pickle
import copy

#sys.setrecursionlimit(5)

def deep_hash(obj):
    """ deep_hash creates a hash from the object

    """
    pass

def deep_cmp(obj1, obj2):
    """ deep_cmp compares two objects deeply

    """
    pass

class tree(object):
    """ a tree is an object's structure
    """
    def __init__(self, obj, skip_patterns=[]):
        self._skip_patterns = ['.' + pttrn for pttrn in skip_patterns]
        self._dict = {}
        self.parent = '.'
        self.inspected = []
        self.deep_inspect(obj)

    def deep_inspect(self, obj):
        #obj = self.resolve_weak_ref(obj, parent)
        if len(inspect.getmembers(obj)) > 1:
            arr = inspect.getmembers(obj) #obj.__dict__
            _arr = {}
            for member in arr:
                _arr[member[0]] = member[1]
            arr = _arr
            if hasattr(obj, '__dict__'):
                dictarr = obj.__dict__
                combarr = arr.copy()
                combarr.update(dictarr)
                arr = combarr
            for key, member in arr.iteritems():
                if inspect.isfunction(member):
                    pass
                elif inspect.ismethod(member):
                    pass
                elif inspect.isbuiltin(member):
                    pass
                elif inspect.isclass(member):
                    pass
                elif inspect.istraceback(member):
                    pass
                elif inspect.isroutine(member):
                    pass
                elif repr(member) in self.inspected:
                    pass
                elif key[0] == '_':
                    pass
                elif hasattr(member, '__dict__') or len(inspect.getmembers(member)) > 1:
                    self.inspected.extend([repr(member)])
                    self.parent  = self.parent + key + '.'
                    self.deep_inspect(member)
                else:
                    self.parent = self.parent + key + '.'
                    self.itermember(member)
        else:
            self.itermember(obj)

    def itermember(self, obj):
        if self.parent not in self._skip_patterns:
            self._dict[self.parent] = self.typesize(obj)

    def resolve_weak_ref(self, obj):
        if hasattr(obj, '__weakref__'):
            #print parent + 'weakref' + str(type(obj))
            try:
                obj = obj.__weakref__()
                #print parent + 'weakref' + repr(obj)
                return obj.__weakref__()
            except TypeError:
                return obj

    def typesize(self, obj):
        string = repr(obj)
        try:
            pickle.pickle(obj)
        except PicklingError:
            string = str(type(obj)) + str(sys.getsizeof(obj))
        if pickle.dumps(obj) != pickle.dumps(copy.copy(obj)):
            string = str(type(obj)) + str(sys.getsizeof(obj))
        return string

    def diff(self, tree2):
        if not isinstance(tree2, tree):
            tree2 = tree(tree2)
        if self.string() != tree2.string():
            for key, val in self._dict.iteritems():
                if key not in tree2._dict.keys():
                    print "1%s: %15s | 2%s: %15s" % (key, key, None, None)
                elif val != tree2._dict[key]:
                    print "1%s: %15s | 2%s: %15s" % (key, val, key, tree2._dict[key])

    def __eq__(self, tree2):
        if not isinstance(tree2, tree):
            tree2 = tree(tree2)
        return self.string() == tree2.string()

    def string(self):
        """ returns the string representation of the object """
        return str(self._dict)

    def hash(self):
        """ returns the hash of the object and all its members"""
        return hashlib.sha1(str(self._dict))
