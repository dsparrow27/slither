from slither import api


class LessThanOrEqualToNode(api.ComputeNode):
    Type = "LessThanOrEqualToNode"
    value1 = api.AttributeDefinition("kFloat", isInput=True)
    value2 = api.AttributeDefinition("kFloat", isInput=True)
    result = api.AttributeDefinition(api.types.kBoolean, isOutput=True)

    def execute(self):
        result = self.value1.value() <= self.value2.value()

        self.result.setValue(result)
