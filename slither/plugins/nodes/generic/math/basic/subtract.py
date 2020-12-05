from slither import api


class Substract(api.ComputeNode):
    Type = "substract"

    def execute(self, context):
        context.output.setValue(context.inputA.value() - context.inputB.value())
