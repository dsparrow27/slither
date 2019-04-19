from slither import api


class InRangeNode(api.ComputeNode):
    Type = "InRangeNode"
    value1 = api.AttributeDefinition("kFloat", isInput=True)
    value2 = api.AttributeDefinition("kFloat", isInput=True)
    result = api.AttributeDefinition(api.types.kBoolean, isOutput=True)

    def execute(self):
        result = self.value1.value() in range(self.value2.value())

        self.result.setValue(result)
