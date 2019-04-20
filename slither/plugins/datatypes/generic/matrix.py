from slither.core import types


class Matrix4(types.DataType):
    Type = "kMatrix4"

    def __init__(self, matrix):
        super(Matrix4, self).__init__(matrix)

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, self._value)

    def __eq__(self, other):
        """Compares the left with the right of the operator
        :param other: Matrix
        :return: boolean
        """
        return isinstance(other, self) and self._value == other.value

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
        """Substracts the right from the left of the operator
        :param other: Matrix
        """
        raise NotImplementedError

    def __mul__(self, other):
        """Multiples the matrix
        :param other: Matrix
        """
        for i in xrange(len(self.matrix)):
            for axis in xrange(len(self.matrix[i])):
                self._value[i][axis] *= other[i, axis]
        return self

    def __neg__(self):
        raise NotImplementedError

    def toIdentity(self):
        """Sets the matrix identity
        :return:
        """
        self._value = [[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]]
        return self

    def clear(self):
        """Sets the matrix to [[0,0,0,0],[0,0,0,0],[0,0,0,0], [0,0,0,0]]
        """
        self._value = [[0, 0, 0] for i in xrange(len(self._value))]

    def translate(self):
        """Returns the translation component of this matrix
        """
        raise NotImplementedError

    def scale(self):
        raise NotImplementedError

    def rotate(self):
        raise NotImplementedError
