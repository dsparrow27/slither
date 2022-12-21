import sys, os
from zoo.core import api as zooapi


def runTests():
    from tests import runtests
    testPath = os.path.dirname(runtests.__file__)
    os.environ["TEST_PATH"] = testPath
    runtests.main()


def main():
    cfg = zooapi.zooFromPath(os.environ["ZOOTOOLS_PRO_ROOT"])
    cfg.resolver.resolveFromPath(cfg.resolver.environmentPath())
    runTests()


def parseArguments(args):
    main()


if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    parseArguments(sys.argv[1:])
