class AttributeAlreadyConnected(Exception):
    def __init__(self, input, output, *args, **kwargs):
        msg = "Input Plug '{}' already connected to {}".format(input.name(), output.name())
        super(AttributeAlreadyConnected, self).__init__(msg, *args, **kwargs)

class AttributeCompatiblityError(Exception):
    def __init__(self, attr1, attr2, *args, **kwargs):
        msg = "The Given attributes aren't compatible {} - {}".format(attr1.name(), attr2.name())
        super(AttributeCompatiblityError, self).__init__(msg, *args, **kwargs)
