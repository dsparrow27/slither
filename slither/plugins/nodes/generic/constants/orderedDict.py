from collections import OrderedDict

from slither import api


class OrderDict(api.ComputeNode):
    Type = "OrderDict"
    category = "constant"
    documentation = "OrderedDict"
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kDict, default=OrderedDict())

    def execute(self, context):
        self.output.setValue(OrderedDict(self.value.value()))
