from collections import OrderedDict

from slither.core import attribute
from slither.core import node


class OrderDict(node.BaseNode):
    category = "constant"
    documentation = "OrderedDict"
    output = attribute.OutputDefinition(type_=dict, default=OrderedDict())

    def execute(self):
        self.output.setValue(OrderedDict(self.value.value()))
