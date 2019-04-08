from collections import OrderedDict

from slither.core import attribute
from slither.core import node


class OrderDict(node.BaseNode):
    Type = "OrderDict"
    category = "constant"
    documentation = "OrderedDict"
    output = attribute.AttributeDefinition(isOutput=True, type_="dict", default=OrderedDict())

    def execute(self):
        self.output.setValue(OrderedDict(self.value.value()))
