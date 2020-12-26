from slither import api


class Power(api.PXComputeNode):
    Type = "power"
    def compute(self, context):
        context.output.setValue(context.inputA.value() ** context.inputB.value())
