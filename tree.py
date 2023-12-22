from abc import ABC, abstractmethod
from typing import Optional, List


class Node(ABC):
    """
    An abstract node class for use with the binary tree
    """
    def __init__(self):
        super().__init__()
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.parent: Optional[Node] = None

    @abstractmethod
    def value(self) -> int:
        pass

    def __lt__(self, other) -> bool:
        return isinstance(other, Node) and self.value() < other.value()
    
    def __gt__(self, other) -> bool:
        return isinstance(other, Node) and self.value() > other.value()
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Node) and self.value() == other.value()


class BinaryTree:
    """
    represents a binary tree, which can be used to find intervals of Boids
    for faster execution
    """
    def __init__(self):
        self.root = None

    def add_node(self, n: Node):
        """
        adds a node to the tree
        """
        if self.root is None:
            self.root = n
            return
        
        current = self.root
        while True:
            if n > current:
                if current.right == None:
                    current.right = n
                    n.parent = current
                    return
                current = current.right
                continue
            
            if n <= current:
                if current.left == None:
                    current.left = n
                    n.parent = current
                    return
                current = current.left

    @staticmethod
    def min(n: Optional[Node]) -> Optional[Node]:
        """
        returns the smallest element in the tree, this is the left most node
        """
        if n is None:
            return None
        current = n
        while current.left is not None: current = current.left
        return current
    
    @staticmethod
    def max(n: Optional[Node]) -> Optional[Node]:
        """
        returns the largest element in the tree, this is the right most node
        """
        if n is None:
            return None
        current = n
        while current.right is not None: current = current.right
        return current
    
    @staticmethod
    def recheck_position(n: Optional[Node]):
        """
        re checks that n satisfies the binary tree constraint

        only checks for the current node and does not check other nodes
        """
        v = n.value()
        current = n
        while True:
            if current.right is not None and v > current.right.value():
                # we're larger than the right child, move to the right
                current = current.right
            elif current.left is not None and v < current.left.value():
                # we're smaller than the left child, move to the left
                current = current.left
            elif current.parent is not None:
                if current.parent.right is current and v < current.parent.value():
                    # we're the parent's right child and we're smaller than the parent, move up
                    current = current.parent
                elif current.parent.left is current and v > current.parent.value():
                    # we're the parent's left child and we're larger than the parent, move up
                    current = current.parent
            else:
                break

        # Rotates the current node to the right
        #
        # F            F
        #  \            \
        #   A            B
        #  / \          / \
        # C   B   =>   D   A
        #    / \      /     \
        #   D   E    C       E
        #
        l = n.left
        if l is not None:
            BinaryTree.min(n.right).left = l
        n.right.parent = n.parent
        n.right = n.right.right
        n.left = None
        
    
    def find_lower_limit(self, limit: int) -> Optional[Node]:
        """
        finds the smallest node that has a value larger than or equal to the given limit
        """
        if self.root is None:
            return None
        
        current = self.root
        while True:
            if limit <= current.value():
                if current.left is not None:
                    current = current.left
                else:
                    return current
            
            if limit > current.value():
                if current.right is not None:
                    current = current.right
                else:
                    if current.parent is not None and current.parent.left is current:
                        return current.parent
                    return None

    def find_interval(self, lower: int, upper: int) -> List[Node]:
        """
        finds the set of nodes in the range [lower, upper] (inclusive)
        """
        current = self.find_lower_limit(lower)
        if current is None:
            return []
        
        result = []
        while current.value() <= upper:
            result.append(current)
            if current.right is not None:
                # step right (and possible left)
                current = self.min(current.right)
            else:
                # backtrack to the next node larger than this one
                while current.parent is not None and current.parent.right is current: current = current.parent
                if current.parent is None:
                    # we hit the end of the tree
                    break
                current = current.parent

        return result


