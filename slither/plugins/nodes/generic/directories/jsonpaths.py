import json
import os

from slither import api


class LoadJson(api.PXComputeNode):
    Type = "loadJson"
    def compute(self, context):
        filePath = context.path.value()
        if not filePath.exists():
            raise ValueError("File Path doesn't exist!: {}".format(filePath))
        with open(filePath, "r") as f:
            context.output.setValue(json.load(f))


class SaveJson(api.PXComputeNode):
    Type = "saveJson"
    def compute(self, context):
        filePath = context.path.value()
        if not os.path.dirname(filePath.exists()):
            raise ValueError("File Path doesn't exist!: {}".format(filePath))
        with open(filePath, "w") as f:
            json.dump(context.inputData.value(), f)
