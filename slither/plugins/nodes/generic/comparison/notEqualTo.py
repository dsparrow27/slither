from slither import api


class NotEqualToNode(api.ComputeNode):
    Type = "NotEqualToNode"
    value1 = api.AttributeDefinition(api.types.kFloat, isInput=True)
    value2 = api.AttributeDefinition(api.types.kFloat, isInput=True)
    result = api.AttributeDefinition(api.types.kBool, isOutput=True)

    def execute(self):
        result = self.value1.value() != self.value2.value()

        self.result.setValue(result)
