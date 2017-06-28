"""This module deals with module paths, importing and the like.
"""
import inspect
import logging
import os
import sys
logger = logging.getLogger(__name__)


def importModule(modulePath, name=""):
    if isDottedPath(modulePath) or not os.path.exists(modulePath):
        try:
            return __import__(modulePath, fromlist="dummy")
        except ImportError:
            pass

    try:
        import imp
        if os.path.exists(modulePath):
            if not name:
                name = os.path.splitext(os.path.basename(modulePath))[0]
            if name in sys.modules:
                return sys.modules[name]
            return imp.load_source(name, os.path.realpath(modulePath))
    except ImportError:
        logger.error("failed to import {}".format(modulePath), exc_info=True)
        return None
    except IOError:
        logger.error("failed to import {}".format(modulePath), exc_info=True)
        return None


def iterModules(path, exclude=None):
    """Iterate of the modules of a given folder path
    :param path: str, The folder path to iterate
    :param exclude: list, a list of files to exclude
    :return: iterator
    """
    if not exclude:
        exclude = []
    _exclude = ["__init__.py", "__init__.pyc"]
    for root, dirs, files in os.walk(path):
        if "__init__.py" not in files:
            continue
        for f in files:
            basename = os.path.basename(f)[0]
            if f not in _exclude and basename not in exclude:
                modulePath = os.path.join(root, f)
                if f.endswith(".py") or f.endswith(".pyc"):
                    yield modulePath


def iterMembers(module, predicate=None):
    """Iterates the members of the module, use predicte to restrict to a type
    :param module:Object, the module object to iterate
    :param predicate: inspect.class
    :return:iterator
    """
    for mod in inspect.getmembers(module, predicate=predicate):
        yield mod


def isDottedPath(path):
    """Determines if the path is a dotted path. Bit of a hack
    :param path: str
    :return: bool
    """
    return len(path.split(".")) > 1

