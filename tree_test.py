import unittest
from tree import BinaryTree, Node


class TestNode(Node):
    def __init__(self, v: int):
        super().__init__()
        self.v = v

    def value(self) -> int:
        return self.v
    

class TestBinaryTree(unittest.TestCase):
    def test_add(self):
        t = BinaryTree()
        data = [5, 7, 6, 3, 4, 2]
        for d in data:
            t.add_node(TestNode(d))

        self.assertEqual(t.root.value(), 5, 'verifying root of binary tree element 5')
        self.assertEqual(t.root.right.value(), 7, 'verifying binary tree element 7')
        self.assertEqual(t.root.right.left.value(), 6, 'verifying binary tree element 6')
        self.assertEqual(t.root.left.value(), 3, 'verifying binary tree element 3')
        self.assertEqual(t.root.left.right.value(), 4, 'verifying binary tree element 4')
        self.assertEqual(t.root.left.left.value(), 2, 'verifying binary tree element 2')

        output = t.traverse_values()
        self.assertEqual(output, [2, 3, 4, 5, 6, 7], 'tree should traverse correctly')
