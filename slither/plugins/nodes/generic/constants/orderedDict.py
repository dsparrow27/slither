from collections import OrderedDict

from slither import api


class OrderDict(api.PXComputeNode):
    Type = "orderDict"
    # category = "constant"
    # documentation = "OrderedDict"
    # output = api.AttributeDefinition(output=True, type_=api.types.kDict, default=OrderedDict())

    def compute(self, context):
        context.output.setValue(OrderedDict(context.value.value()))
