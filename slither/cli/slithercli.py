import argparse
import sys, os
from zoo.core import api as zooapi


def runTests():
    from tests import runtests
    testPath = os.path.dirname(runtests.__file__)
    os.environ["TEST_PATH"] = testPath
    runtests.main()


def executeGraph(filePath):
    filePath = os.path.abspath(os.path.expandvars(os.path.expanduser(filePath)))
    if not os.path.exists(filePath):
        raise FileNotFoundError(filePath)

    from slither import api

    app = api.Application()
    graph = app.createGraphFromPath(name="cliGraph", filePath=filePath)
    graph.execute(graph.root, "inProcess")  # temp


def main(args):
    cfg = zooapi.zooFromPath(os.environ["ZOOTOOLS_ROOT"])
    cfg.resolver.resolveFromPath(cfg.resolver.environmentPath())
    if args.test:
        runTests()
        return
    executeGraph(args.graph)


def parseArguments(args):
    parser = argparse.ArgumentParser("Slither")
    parser.add_argument("--graph", "-g",
                        type=str, help="Graph to load and execute")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args(args)
    main(args)


if __name__ == "__main__":
    parseArguments(None)
