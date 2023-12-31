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

        self.assertEqual(len(t), 6, 'length of the tree should be correct')

    def test_deletion(self):

        testdata = [5, 8, 6, 7, 3, 4, 2, 10, 9]

        """
             5
           /   \
          3      8
         / \   /   \
        2   4 6     10
               \   /
                7 9
        """

        def build_test_tree() -> BinaryTree:
            t = BinaryTree()
            for d in testdata:
                t.add_node(TestNode(d))
            return t

        tc = build_test_tree()
        tc.delete_node(TestNode(17))
        output = tc.traverse_values()
        self.assertEqual(output, list(sorted(testdata)), 'delete when not in the tree should do nothing')

        tc.delete_node(tc.root.right)
        self.assertEqual(len(tc), len(testdata)-1, 'expected correct node count')
        self.assertEqual(tc.root.right.value(), 9, 'expected the correct replacment value when using the min of the right')

        """
             5
           /   \
          3      9
         / \   /   \
        2   4 6     10
               \
                7
        """

        tc.delete_node(tc.root.right)
        self.assertEqual(len(tc), len(testdata)-2, 'expected correct node count')
        self.assertEqual(tc.root.right.value(), 10, 'expected the correct replacment value when using the right child')

        """
             5
           /   \
          3      10
         / \   /   
        2   4 6    
               \
                7
        """

        tc.delete_node(tc.root.right)
        self.assertEqual(len(tc), len(testdata)-3, 'expected correct node count')
        self.assertEqual(tc.root.right.value(), 7, 'expected the correct replacment value when using the max of the left')

        """
             5
           /   \
          3     7
         / \   /   
        2   4 6     
        """

        tc.delete_node(tc.root.right)
        self.assertEqual(len(tc), len(testdata)-4, 'expected correct node count')
        self.assertEqual(tc.root.right.value(), 6, 'expected the correct replacment value when using the left child')

        """
             5
           /   \
          3     6
         / \    
        2   4     
        """

        tc.delete_node(tc.root.right)
        self.assertEqual(len(tc), len(testdata)-5, 'expected correct node count')
        self.assertIsNone(tc.root.right, 'expected the right child to be empty when there are no children')

        """
            5
           /   
          3    
         / \    
        2   4     
        """

        tc.delete_node(tc.root)
        self.assertEqual(len(tc), len(testdata)-6, 'expected correct node count')
        self.assertEqual(tc.root.value(), 4, 'expected the correct replacement when deleting the root')
