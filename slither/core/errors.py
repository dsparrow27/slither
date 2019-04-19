class AttributeAlreadyConnected(Exception):
    def __init__(self, input, output, *args, **kwargs):
        msg = "Input Plug '{}' already connected to {}".format(input.name(), output.name())
        super(AttributeAlreadyConnected, self).__init__(msg, *args, **kwargs)
