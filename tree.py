import numpy as np

class BNode():
    """
    Node of a binary tree.
    """
    def __init__(self, content, left, right):
        self.content = content
        self.left = left
        self.right = right
    
    def __getattr__(self, i):
        if i == 0:
            return self.left
        elif i == 1:
            return self.right
        else:
            raise KeyError('Key Error : index out of range with %s' % i)
    
    def __iter__(self):
        self.idx = 0
        return self
    
    def __next__(self):
        if self.idx > 1:
            raise StopIteration
        else:
            self.idx += 1
            return self.__getettr__(self.idx)
    
    def __repr__(self):
        return ('tree.BNode : content %s' % self.content)
    
    def left_print(self):
        """
        Prints the content of the children nodes after left-first exploration.
        """
        self.left.left_print()
        self.right.left_print()
        print(self.content)

class UNode():
    """
    Node of a unary tree.
    """
    def __init__(self, content, child):
        self.content = content
        self.child = child
    
    def __repr__(self):
        return ('tree.UNode : content %s' % self.content)
    
    def left_print(self):
        """
        Prints the content and child.
        """
        print(self.child)
        print(self.content)

class Tree():
    """
    Class for a tree.
    """
    def __init__(self):
        self.root = root
