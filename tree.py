from abc import ABC, abstractmethod
from typing import Optional, List, Union


class Node(ABC):
    """
    An abstract node class for use with the binary tree
    """
    def __init__(self):
        super().__init__()
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.parent: Optional[Node] = None

    def __repr__(self) -> str:
        return self.value()
    
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    @abstractmethod
    def value(self) -> Union[int, float]:
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
    
    def __repr__(self) -> str:
        lines = ['tree:']
        if self.count == 0:
            return 'tree: empty'
        
        lines.append(f'root: {self.root.value()}')

        stack = [(self.root.right, True, 1), (self.root.left, False, 1)]
        while len(stack) > 0:
            node, right, depth = stack[-1]
            stack = stack[:-1]

            indent = '\t'*depth

            if node is None:
                lines.append(f'{indent}{"right" if right else "left"}: None')
                continue

            lines.append(f'{indent}{"right" if right else "left"}: {node.value()}')

            stack.append((node.right, True, depth+1))
            stack.append((node.left, False, depth+1))
        return '\n'.join(lines)

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
    
    def transplant(self, x: Node, y: Optional[Node]):
        if x.parent is None:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        if y is not None:
            y.parent = x.parent
    
    def delete_node(self, n: Node):
        """
        removes a node from the tree
        does not check if the node exists within the tree first
        """
        
        if self.count == 1:
            self.root = None
            self.count = 0
            return
        
        if n.is_leaf():
            # the count is > 1 so we cannot be the root node and be a leaf
            if n.parent.left is n:
                n.parent.left = None
            else:
                n.parent.right = None
            self.count -= 1
            return
        
        if n.left is None:
            self.transplant(n, n.right)
        elif n.right is None:
            self.transplant(n, n.left)
        else:
            rep = self.min(n.right)
            if rep.parent is not n:
                self.transplant(rep, rep.right)
                rep.right = n.right
                rep.right.parent = rep
            self.transplant(n, rep)
            rep.left = n.left
            rep.left.parent = rep

        self.count -= 1

    def reinsert_node(self, n: Node):
        """
        first deletes a node from the tree,
        then adds it back into the tree,
        this can be used to update nodes after their values have changed.
        """
        self.delete_node(n)

        # completely detach node to prepare for reinsertion
        n.parent = None
        n.left = None
        n.right = None

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

    def find_interval(self, lower: Union[int, float], upper: Union[int, float]) -> List[Node]:
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


