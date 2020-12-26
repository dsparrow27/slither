import os

from slither import api


class PathExists(api.PXComputeNode):
    Type = "pathExists"
    def compute(self, context):
        context.output.setValue(os.path.exists(context.file.value()))
