from slither import api


class IfNode(api.ComputeNode):
    Type = "ifNode"
    ifTrue = api.AttributeDefinition(type_=api.types.kFloat, isInput=True)
    ifFalse = api.AttributeDefinition(type_=api.types.kFloat, isInput=True)
    condition = api.AttributeDefinition(type_=api.types.kFloat, isInput=True)
    result = api.AttributeDefinition(type_=api.types.kBool, isOutput=True)

    def execute(self, context):
        if self.conditionPlug_.value:
            result = self.ifTruePlug_.value
        else:
            result = self.ifFalsePlug.value

        self.result.setValue(result)
