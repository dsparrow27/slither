class AttributeAlreadyConnectedError(Exception):
    def __init__(self, input, output, *args, **kwargs):
        msg = "Input Plug '{}' already connected to {}".format(input.name(), output.name())
        super(AttributeAlreadyConnectedError, self).__init__(msg, *args, **kwargs)


class AttributeCompatiblityError(Exception):
    def __init__(self, attr1, attr2, *args, **kwargs):
        msg = "The Given attributes aren't compatible {} - {}".format(attr1.name(), attr2.name())
        super(AttributeCompatiblityError, self).__init__(msg, *args, **kwargs)


class UnsupportedConnectionCombinationError(Exception):
    def __init__(self, attr1, attr2, *args, **kwargs):
        msg = "Unsupported connection combination:\n{} - {}".format(attr1.fullName(), attr2.fullName())
        super(UnsupportedConnectionCombinationError, self).__init__(msg, *args, **kwargs)


class NotSupportedAttributeIOError(Exception):
    pass
