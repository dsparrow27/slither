from slither import api


class IfNode(api.PXComputeNode):
    Type = "condition"
    def compute(self, context):
        if context.conditionPlug_.value:
            result = context.ifTruePlug_.value
        else:
            result = context.ifFalsePlug.value

        context.result.setValue(result)
