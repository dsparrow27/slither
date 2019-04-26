from slither import api


class EqualToNode(api.ComputeNode):
    Type = "equalToNode"
    value1 = api.AttributeDefinition(type_=api.types.kFloat, input=True)
    value2 = api.AttributeDefinition(type_=api.types.kFloat, input=True)
    result = api.AttributeDefinition(type_=api.types.kBool, output=True)

    def execute(self, context):
        result = self.value1.value() == self.value2.value()
        self.result.setValue(result)
