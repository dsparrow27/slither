from zoo.libs.plugin import plugin


class ProxyBase(plugin.Plugin):
    Type = ""


class PXComputeNode(ProxyBase):
    def compute(self, context):
        pass


class PXCompoundNode(ProxyBase):
    Type = "compound"

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
