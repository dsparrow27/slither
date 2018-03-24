from slither.core import node
from slither.core import service


class Compound(node.BaseNode):
    """The Compound class encapsulates a set of child nodes, which can include other compounds.
    We provide methods to query the children nodes of the current compound.
    """

    def __init__(self, name, application):
        """
        :param name: The name that this node will have, if the name already exist a number we be appended.
        :type name: str
        """
        super(Compound, self).__init__(name, application=application)
        self.children = []

    @staticmethod
    def isCompound():
        return True

    def __len__(self):
        """returns the number of child nodes for this compound
        :return: int
        """
        return len(self.children)

    def __iter__(self):
        """Returns a generator of the child nodes
        :return: generator
        """
        return iter(self.children)

    def __add__(self, other):
        """Adds the nodes from one compound to this one
        :param other: Compound
        """
        if isinstance(other, Compound):
            for child in other:
                self.addChild(child)

    def __sub__(self, other):
        if isinstance(other, Compound):
            for child in other:
                if child in self.children:
                    self.children.remove(child)

    def __contains__(self, item):
        if item in self.children:
            return True
        return False

    def mutate(self):
        """Special method that allows this node to generate(mutate) other nodes as child nodes this can also contain
        other compounds
        """
        pass

    def child(self, name):
        for child in self:
            if child.name == name:
                return child
            elif child.isCompound():
                return child.child(name)

    def addChild(self, child):
        if child not in self.children:
            self.children.append(child)
            parent = child.parent
            if parent and parent.isCompound() and parent != self:
                parent.removeChild(child)
            child.parent = self
            return True
        return False

    def removeChild(self, child):
        if isinstance(child, str):
            child = self.child(child)

        if child in self:
            child.disconnectAll()
            self.children.remove(child)
            return True
        return False

    def clear(self):
        for child in self.children:
            self.removeChild(child)
        self.children = []

    def hasChild(self, name):
        for i in self:
            if i.name == name:
                return i

    def hasChildren(self):
        return len(self.children) > 0

    def topologicalOrder(self):
        return service.topologicalOrder(self.children)

    def serialize(self):
        data = super(Compound, self).serialize()
        data["children"] = [i.serialize() for i in self.children]
        return data
