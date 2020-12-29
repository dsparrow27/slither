from slither.core import types
from zoovendor.six.moves import range


class Matrix4(types.DataType):
    Type = "kMatrix4"

    def __getitem__(self, pos):
        return self._value[pos]

    def __setitem__(self, pos, value):
        self._value[pos] = value

    def __add__(self, other):
        """Adds the left to the right of the operator
        :param other: Matrix
        """
        raise NotImplementedError

    def __sub__(self, other):
        """Subtracts the right from the left of the operator
        :param other: Matrix
        """
        raise NotImplementedError

    def __mul__(self, other):
        """Multiples the matrix
        :param other: Matrix
        """
        for i in range(len(self._value)):
            for axis in range(len(self._value[i])):
                self._value[i][axis] *= other[i, axis]
        return self

    def __neg__(self):
        raise NotImplementedError

    def toIdentity(self):
        """Sets the matrix identity
        :return:
        """
        self.setValue([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
        return self

    def clear(self):
        """Sets the matrix to [[0,0,0,0],[0,0,0,0],[0,0,0,0], [0,0,0,0]]
        """
        self.setValue([[0, 0, 0]] * len(self._value))

    def translate(self):
        """Returns the translation component of this matrix
        """
        raise NotImplementedError

    def scale(self):
        raise NotImplementedError

    def rotate(self):
        raise NotImplementedError
