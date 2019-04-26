from slither import api


class SplitString(api.ComputeNode):
    Type = "SplitString"
    category = "string"
    documentation = "splits a string by a delimiter"
    string = api.AttributeDefinition(input=True, type_=api.types.kString, default="")
    delimiter = api.AttributeDefinition(input=True, type_=api.types.kString, default=",")
    output = api.AttributeDefinition(output=True, type_=api.types.kString, array=True, default="")

    def execute(self, context):
        self.output.setValue(self.input.value().split(self.delimiter.value()))
