from slither import api


class Multiply(api.PXComputeNode):
    Type = "multiply"
    def compute(self, context):
        context.output.setValue(context.inputA.value() * context.inputB.value())
