from slither import api


class IfNode(api.PXComputeNode):
    Type = "condition"
    # ifTrue = api.AttributeDefinition(type_=api.types.kFloat, input=True)
    # ifFalse = api.AttributeDefinition(type_=api.types.kFloat, input=True)
    # condition = api.AttributeDefinition(type_=api.types.kFloat, input=True)
    # result = api.AttributeDefinition(type_=api.types.kBool, output=True)

    def compute(self, context):
        if context.conditionPlug_.value:
            result = context.ifTruePlug_.value
        else:
            result = context.ifFalsePlug.value

        context.result.setValue(result)
