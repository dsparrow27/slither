from slither.core import attribute
from slither.core import node


class Divide(node.BaseNode):
    category = "math"
    documentation = "Divides the input values together, raises ZooDivisionError if dividing by 0"
    inputA = attribute.InputDefinition(type_=float, default=0)
    inputB = attribute.InputDefinition(type_=float, default=0)
    output = attribute.OutputDefinition(type_=float, default=0)

    def execute(self):
        # @todo log
        try:
            self.output.setValue(self.inputA.value() / self.inputB.value())
        except ZeroDivisionError:
            raise

