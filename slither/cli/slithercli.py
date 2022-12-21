import argparse
import sys, os
from zoo.core import api as zooapi


def runTests():
    from tests import runtests
    testPath = os.path.dirname(runtests.__file__)
    os.environ["TEST_PATH"] = testPath
    runtests.main()


def executeGraph(filePath, scheduler):
    filePath = os.path.abspath(os.path.expandvars(os.path.expanduser(filePath)))
    if not os.path.exists(filePath):
        raise FileNotFoundError(filePath)

    from slither import api

    app = api.Application()
    graph = app.createGraphFromPath(name="cliGraph", filePath=filePath)
    graph.execute(graph.root, scheduler)  # temp


def main(args):
    cfg = zooapi.zooFromPath(os.environ["ZOOTOOLS_PRO_ROOT"])
    cfg.resolver.resolveFromPath(cfg.resolver.environmentPath())
    if args.test:
        runTests()
        return
    executeGraph(args.graph, args.scheduler)


def parseArguments(args):
    print(args)
    parser = argparse.ArgumentParser("Slither")
    parser.add_argument("--graph", "-g",
                        type=str, help="Graph to load and execute")
    parser.add_argument("--scheduler", "-s",
                        default="inProcess",
                        type=str, help="Scheduler default name")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args(args)
    main(args)


if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    parseArguments(sys.argv[1:])
