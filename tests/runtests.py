import os
import sys
import logging
from zoo.core import api

cfg = api.zooFromPath(os.environ["ZOOTOOLS_ROOT"])
cfg.resolver.resolveFromPath(cfg.resolver.environmentPath())
logging.basicConfig(level=logging.DEBUG)


def main():
    from zoo.libs.utils import unittestBase
    try:
        result = unittestBase.runTests(os.environ["TEST_PATH"].split(os.pathsep))
        if result is None or not result.wasSuccessful():
            raise Exception("Failed Unittests")
        sys.exit(0)
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()
