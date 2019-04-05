from slither.core import attribute
from slither.core import node


class GreaterThanOrEqualToNode(node.BaseNode):
    Type = "GreaterThanOrEqualToNode"
    value1 = attribute.AttributeDefinition(float, isInput=True)
    value2 = attribute.AttributeDefinition(float, isInput=True)
    result = attribute.AttributeDefinition(bool, isOutput=True)

    def execute(self):
        result = self.value1Plug_ >= self.value2Plug_
        self.result.setValue(result)
