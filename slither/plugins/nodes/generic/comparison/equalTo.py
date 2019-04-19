from slither import api


class EqualToNode(api.ComputeNode):
    Type = "equalToNode"
    value1 = api.AttributeDefinition(type_=api.types.kFloat, isInput=True)
    value2 = api.AttributeDefinition(type_=api.types.kFloat, isInput=True)
    result = api.AttributeDefinition(type_=api.types.kBool, isOutput=True)

    def execute(self):
        result = self.value1.value() == self.value2.value()
        self.result.setValue(result)
