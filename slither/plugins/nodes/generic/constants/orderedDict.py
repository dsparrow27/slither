from collections import OrderedDict

from slither import api


class OrderDict(api.ComputeNode):
    Type = "orderDict"
    # category = "constant"
    # documentation = "OrderedDict"
    # output = api.AttributeDefinition(output=True, type_=api.types.kDict, default=OrderedDict())

    def execute(self, context):
        context.output.setValue(OrderedDict(context.value.value()))
