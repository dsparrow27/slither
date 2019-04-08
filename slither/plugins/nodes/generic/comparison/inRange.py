from slither.core import attribute
from slither.core import node


class InRangeNode(node.BaseNode):
    Type = "InRangeNode"
    value1 = attribute.AttributeDefinition("float", isInput=True)
    value2 = attribute.AttributeDefinition("float", isInput=True)
    result = attribute.AttributeDefinition("bool", isOutput=True)

    def execute(self):
        result = self.value1.value() in range(self.value2.value())

        self.result.setValue(result)
