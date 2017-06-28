import json
import logging

logger = logging.getLogger(__name__)


def isIteratable(obj):
    try:
        for i in iter(obj):
            return True
    except TypeError:
        return False



def loadJson(filePath):
    """
    This procedure loads and returns the data of a json file

    :return type{dict}: the content of the file
    """
    # load our file
    try:
        with open(filePath) as f:
            data = json.load(f)
    except Exception as er:
        logger.debug("file (%s) not loaded" % filePath)
        raise er
    # return the files data
    return data


def saveJson(data, filepath, **kws):
    """
    This procedure saves given data to a json file

    :param kws: Json Dumps arguments , see standard python docs
    """

    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, **kws)
    except IOError:
        logger.error("Data not saved to file {}".format(filepath))
        return False

    logger.info("------->> file correctly saved to : {0}".format(filepath))

    return True

