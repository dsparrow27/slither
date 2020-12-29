import math

from slither.core import types


class Vector(types.DataType):
    """Basic Vector Object
    """
    Type = "kVector2D"

    def __init__(self, value=None, default=None):
        """
        :param vec: list
        """
        super(Vector, self).__init__(value or [0, 0], default=default or [0, 0])

    def setValue(self, value):
        if len(value) != len(self._value):
            raise ValueError("Incorrect value length must be size 2")
        return super(Vector, self).setValue(value)

    def __len__(self):
        """Returns the length, if its a vector2d then length 2 will be returned
        :return:
        """
        return len(self.value())

    def __getitem__(self, item):
        """Gets the index value from the vector
        :param item: int, the index value in the vector to get
        :return: float or int
        """
        return self.value()[item]

    def __setitem__(self, key, value):
        """Sets the value within the vector via the index
        :param key:
        :param value:
        """
        self._value[key] = value

    def __add__(self, vec):
        """Adds two vectors together and the returns the resulting example
        :param vec: Vector2D or flost3
        :return: Vector2D
        """
        assert len(self) == len(vec)
        return Vector([self.value()[i] + vec[i] for i in range(len(self))])

    def __sub__(self, vec):
        """Subtracts the two vectors
        :param vec: Vector2D
        :return: Vector2D
        """
        return self + (-vec)

    def __neg__(self):
        """Negates the vector
        :return: new Vector
        """
        return Vector([vec * -1 for vec in self.value()])

    def __mul__(self, vec):
        """Dot product(scalar product) of two vectors. Takes Two equal length vectors and returns a single number.
        :param vec: Vector2D instance or float3
        :return: new Vector
        """
        assert len(self) == len(vec)
        return sum(Vector([self.value()[i] * vec[i] for i in range(len(self.value()))]))

    def __rmul__(self, scalar):
        """Vector right multiplication
        :param scalar: float or int
        :return: new Vector
        """
        return Vector([x * scalar for x in self.value()])

    def __abs__(self):
        return Vector([abs(i) for i in self.value()])

    def length(self):
        """Return the length of the vector
        :return: float
        """
        return math.sqrt(sum(x * x for x in self.value()))

    def normalize(self):
        """Returns the normalized vector, modifies the original vec
        :return:
        """
        length = self.length()
        value = self.value()
        value[0] = value[0] / length
        value[1] = value[1] / length
        self.setValue(value)
        return self

    def rotate(self, angle):
        """Rotate the vector by the angle
        :param angle:
        """
        cos = math.cos(angle)
        sin = math.sin(angle)
        value = self.value()
        return Vector([value[0] * cos - value[1] * sin, value[0] * sin + value[1] * cos])

    @property
    def x(self):
        """Returns the x axis of the vector
        :return: int or float
        """
        return self.value()[0]

    @property
    def y(self):
        """Returns the y axis of the vector
        :return: int or float
        """
        return self.value()[1]

    @x.setter
    def x(self, value):
        """Sets the x axis of the vector
        """
        self._value[0] = value

    @y.setter
    def y(self, value):
        """Sets the y axis of the vector
        """
        self._value[1] = value


class Vector3D(Vector):
    Type = "kVector3D"

    def __init__(self, value=None, default=None):
        """
        :param vec: list
        """
        super(Vector, self).__init__(value or [0, 0, 0], default=default or [0, 0, 0])

    def __eq__(self, vec):
        return isinstance(vec, Vector3D) and self.vec == vec.vec

    def __add__(self, vec):
        """Adds two vectors together and the returns the resulting example
        :param vec: Vector2D or flost3
        :return: Vector2D
        """
        assert len(self) == len(vec)
        return Vector3D([self.value()[i] + vec[i] for i in range(len(self))])

    def __neg__(self):
        """Negates the vector
        :return: Vector2D, return the negative of the vector, eg (1,-1,2) == (-1,1,-2)
        """
        return Vector3D([vec * -1 for vec in self.value()])

    def __mul__(self, vec):
        """Dot product(scalar product) of two vectors. Takes Two equal length vectors and returns a single number.
        :param vec: Vector2D instance or float3
        :return: Vector2D
        """
        assert len(self.value()) == len(vec)
        return sum(Vector3D([self.value()[i] * vec[i] for i in range(len(self))]))

    def __rmul__(self, scalar):
        """Returns the right multiplication
        :param scalar:
        :return:
        """
        return Vector3D([x * scalar for x in self.value()])

    def normalize(self):
        """Returns the normalized vector, modifies the original vec
        :return: self
        """
        length = self.length()
        value = self.value()
        value[0] = value[0] / length
        value[1] = value[1] / length
        value[2] = value[2] / length
        self.setValue(value)
        return self

    def crossProduct(self, vec):
        """Returns the cross product
        :param vec, Vector3D
        :return: Vector3D
        """
        _x, _y, _z = self.value()

        x = _y * vec.z - _z * vec.y
        y = _z * vec.x - _x * vec.z
        z = _x * vec.y - _y * vec.x
        return Vector3D([x, y, z])

    def rotate(self, rotation):
        """Rotate the vector by the angle using a quaternion
        :param rotation: Quaternion
        """
        w = rotation * rotation.Conjugate()
        return Vector3D([w.x, w.y, w.z])

    def lerp(self, vec, lerpFactor):
        """
        :param vec: Vector3D
        :param lerpFactor: float
        :return: float
        """
        return vec - self * lerpFactor + self

    @property
    def z(self):
        """Returns the z axis of the vector
        :return: int or float
        """
        return self._value[2]

    @z.setter
    def z(self, value):
        """Sets the x axis of the vector
        """
        self._value[2] = value
