if __name__ == '__main__':
    import pprint, logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())
    from slither import startup

    startup.startup()
    from tests import graphtest

    root = graphtest.run()
    pprint.pprint(root.serialize())
    print root.execution.value()
