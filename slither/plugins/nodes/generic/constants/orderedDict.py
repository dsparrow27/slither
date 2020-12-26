from collections import OrderedDict

from slither import api


class OrderDict(api.PXComputeNode):
    Type = "orderDict"
    def compute(self, context):
        context.output.setValue(OrderedDict(context.value.value()))
