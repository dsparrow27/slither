from slither import api


class Substract(api.PXComputeNode):
    Type = "substract"

    def compute(self, context):
        context.output.setValue(context.inputA.value() - context.inputB.value())
