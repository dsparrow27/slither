from slither import api


class Scalar(api.PXComputeNode):
    Type = "scalar"

    def compute(self, context):
        context.output.setValue(float(context.value.value()))
