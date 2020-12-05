from slither import api


class Scalar(api.ComputeNode):
    Type = "scalar"

    def execute(self, context):
        context.output.setValue(float(context.value.value()))
