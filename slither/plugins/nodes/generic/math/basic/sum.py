from slither import api


class Sum(api.PXComputeNode):
    Type = "sum"

    def compute(self, context):
        context.output.setValue(context.inputA.value() + context.inputB.value())
