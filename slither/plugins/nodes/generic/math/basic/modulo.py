from slither import api


class Modulo(api.PXComputeNode):
    Type = "modulo"
    def compute(self, context):
        context.output.setValue(context.inputA.value() % context.inputB.value())
