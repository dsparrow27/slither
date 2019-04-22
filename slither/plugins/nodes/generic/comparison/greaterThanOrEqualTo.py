from slither import api


class GreaterThanOrEqualToNode(api.ComputeNode):
    Type = "greaterThanOrEqualToNode"
    value1 = api.AttributeDefinition(type_=api.types.kFloat, isInput=True)
    value2 = api.AttributeDefinition(type_=api.types.kFloat, isInput=True)
    result = api.AttributeDefinition(type_=api.types.kBool, isOutput=True)

    def execute(self, context):
        result = self.value1Plug_ >= self.value2Plug_
        self.result.setValue(result)
