from slither import api


class InRangeNode(api.ComputeNode):
    Type = "InRangeNode"
    value1 = api.AttributeDefinition(api.types.kFloat, input=True)
    value2 = api.AttributeDefinition(api.types.kFloat, input=True)
    result = api.AttributeDefinition(api.types.kBool, output=True)

    def execute(self, context):
        result = self.value1.value() in range(self.value2.value())

        self.result.setValue(result)
