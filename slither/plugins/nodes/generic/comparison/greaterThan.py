from slither import api


class GreaterThanNode(api.ComputeNode):
    Type = "greaterThanNode"
    value1 = api.AttributeDefinition(type_=api.types.kFloat, isInput=True)
    value2 = api.AttributeDefinition(type_=api.types.kFloat, isInput=True)
    result = api.AttributeDefinition(type_=api.types.kBool, isOutput=True)

    def execute(self, context):
        result = self.value1.value() > self.value2.value()

        self.result.setValue(result)
