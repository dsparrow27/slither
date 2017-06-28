from slither.core import node
from slither.core import attribute


class GreaterThanNode(node.BaseNode):
    value1 = attribute.InputDefinition(float)
    value2 = attribute.InputDefinition(float)
    result = attribute.OutputDefinition(bool)

    def execute(self):
        result = self.value1.value() > self.value2.value()

        self.result.setValue(result)
