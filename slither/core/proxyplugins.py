from zoo.libs.plugin import plugin


class ProxyBase(plugin.Plugin):
    Type = ""


class PXComputeNode(ProxyBase):
    def compute(self, context):
        pass


class PXCompoundNode(ProxyBase):
    Type = "compound"

    def mutate(self):
        """Special method that allows this node to generate(mutate) other nodes as child nodes this can also contain
        other compounds
        """
        pass

    def compute(self, context):
        pass


class PXPinNode(ProxyBase):
    Type = "pin"

    def compute(self, context):
        pass


class PXCommentNode(ProxyBase):
    Type = "comment"

    def compute(self, context):
        pass
