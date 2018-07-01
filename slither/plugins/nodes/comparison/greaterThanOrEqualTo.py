from slither.core import node
from slither.core import attribute


class GreaterThanOrEqualToNode(node.BaseNode):
    value1 = attribute.AttributeDefinition(float, isInput=True)
    value2 = attribute.AttributeDefinition(float, isInput=True)
    result = attribute.AttributeDefinition(bool, isOutput=True)

    def execute(self):
        result = self.value1Plug_ >= self.value2Plug_
        self.result.setValue(result)
