from slither import api


class Divide(api.PXComputeNode):
    Type = "divide"
    def compute(self, context):
        # @todo log
        try:
            context.output.setValue(context.inputA.value() / context.inputB.value())
        except ZeroDivisionError:
            raise
