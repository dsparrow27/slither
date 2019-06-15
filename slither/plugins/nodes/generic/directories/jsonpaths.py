import json
import os

from slither import api


class LoadJson(api.ComputeNode):
    Type = "LoadJson"
    category = "files"
    documentation = "Loads a json file"
    path = api.AttributeDefinition(input=True, type_=api.types.kFile, default="",
                                   required=True)
    output = api.AttributeDefinition(output=True, type_=api.types.kDict, array=False, default=[])

    def execute(self, context):
        filePath = context.path.value()
        if not filePath.exists():
            raise ValueError("File Path doesn't exist!: {}".format(filePath))
        with open(filePath, "r") as f:
            context.output.setValue(json.load(f))


class SaveJson(api.ComputeNode):
    Type = "SaveJson"
    category = "files"
    documentation = "Save a json file from a dict"
    inputData = api.AttributeDefinition(input=True, type_=api.types.kDict, default="",
                                        required=True)
    path = api.AttributeDefinition(input=True, type_=api.types.kFile, default="",
                                   required=True)

    def execute(self, context):
        filePath = context.path.value()
        if not os.path.dirname(filePath.exists()):
            raise ValueError("File Path doesn't exist!: {}".format(filePath))
        with open(filePath, "w") as f:
            json.dump(context.inputData.value(), f)
