from slither.core import attribute
from slither.core import node


class EqualToNode(node.BaseNode):
    Type = "EqualToNode"
    value1 = attribute.AttributeDefinition(float, isInput=True)
    value2 = attribute.AttributeDefinition(float, isInput=True)
    result = attribute.AttributeDefinition(bool, isOutput=True)

    def execute(self):
        result = self.value1.value() == self.value2.value()
        self.result.setValue(result)
