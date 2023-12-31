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
    
    def __le__(self, other) -> bool:
        return isinstance(other, Node) and self.value() <= other.value()


class BinaryTree:
    """
    represents a binary tree, which can be used to find intervals of Boids
    for faster execution
    """
    def __init__(self):
        self.root = None
        self.count = 0

    def __len__(self) -> int:
        return self.count

    def __contains__(self, obj: Node) -> bool:
        if len(self) == 0: return False

        current = self.root
        while obj is not current:
            if obj <= current:
               if current.left is None: return False
               current = current.left
            else:
                if current.right is None: return False
                current = current.right

        return True 

    def add_node(self, n: Node):
        """
        adds a node to the tree
        """
        if self.root is None:
            self.root = n
            self.count += 1
            return
        
        current = self.root
        while True:
            if n > current:
                if current.right == None:
                    current.right = n
                    n.parent = current
                    self.count += 1
                    return
                current = current.right
                continue
            
            if n <= current:
                if current.left == None:
                    current.left = n
                    n.parent = current
                    self.count += 1
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
    
    def delete_node(self, n: Node):
        """
        removes a node from the tree, if it exists
        """
        if n not in self:
            return
        
        if self.count == 1:
            self.root = None
            self.count = 0
            return
        
        if n.right is None and n.left is None:
            # there are no children
            # the count is > 1 so we cannot be the root node and be a leaf
            if n.parent.right is n:
                n.parent.right = None
            else:
                n.parent.left = None
            n.parent = None
            self.count -= 1
            return

        replacement = self.min(n.right)
        if replacement is None:
            replacement = self.max(n.left)

        # detach replacement node
        if replacement.parent is not None:
            if replacement.parent.right is replacement:
                replacement.parent.right = None
            else:
                replacement.parent.left = None
        replacement.parent = None  # we know at this point one of these must not be None

        if n is self.root:
            self.root = replacement

        replacement.parent = n.parent
        if n.right is not replacement: replacement.right = n.right
        if n.left is not replacement: replacement.left = n.left

        if n.parent is not None:
            if n.parent.right is n:
                n.parent.right = replacement
            else:
                n.parent.left = replacement

        self.count -= 1

    def reinsert_node(self, n: Node):
        """
        first deletes a node from the tree,
        then adds it back into the tree,
        this can be used to update nodes after their values have changed.
        """
        self.delete_node(n)
        self.add_node(n)
    
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
    
    def traverse_values(self) -> List[int]:
        if self.count == 0:
            return []
        
        if self.count == 1:
            return [self.root.value()]
        
        result = []
        current = self.min(self.root)
        while True:
            result.append(current.value())
            if current.right is not None:
                current = self.min(current.right)
            else:
                while current.parent is not None and current.parent.right is current: current = current.parent
                if current.parent is None:
                    break
                current = current.parent

        return result


