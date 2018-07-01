from slither.core import node
from slither.core import attribute


class IfNode(node.BaseNode):
    ifTrue = attribute.AttributeDefinition(float, isInput=True)
    ifFalse = attribute.AttributeDefinition(float, isInput=True)
    condition = attribute.AttributeDefinition(float, isInput=True)
    result = attribute.AttributeDefinition(bool, isOutput=True)

    def execute(self):
        if self.conditionPlug_.value:
            result = self.ifTruePlug_.value
        else:
            result = self.ifFalsePlug.value

        self.result.setValue(result)
