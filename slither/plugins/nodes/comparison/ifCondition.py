from slither.core import node
from slither.core import attribute


class IfNode(node.BaseNode):
    ifTrue = attribute.InputDefinition(float)
    ifFalse = attribute.InputDefinition(float)
    condition = attribute.InputDefinition(float)
    result = attribute.OutputDefinition(bool)

    def execute(self):
        if self.conditionPlug_.value:
            result = self.ifTruePlug_.value
        else:
            result = self.ifFalsePlug.value

        self.result.setValue(result)
