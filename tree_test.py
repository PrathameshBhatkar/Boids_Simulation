import unittest
from tree import BinaryTree, Node


class TestNode(Node):
    def __init__(self, v: int):
        super().__init__()
        self.v = v

    def __repr__(self) -> str:
        return super().__repr__()

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
        self.assertEqual(tc.root.right.value(), 6, 'expected the correct replacment value when using the max of the left')

        """
             5
           /   \
          3     6
         / \     \   
        2   4     7 
        """

        tc.delete_node(tc.root.right)
        self.assertEqual(len(tc), len(testdata)-4, 'expected correct node count')
        self.assertEqual(tc.root.right.value(), 7, 'expected the correct replacment value when using the left child')

        """
             5
           /   \
          3     7
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
        self.assertEqual(tc.root.value(), 3, 'expected the correct replacement when deleting the root')

    def test_reinsertion(self):
        testdata = [1005344, 137029, 1972421, 1937498, 1925201]

        def build_test_tree() -> BinaryTree:
            t = BinaryTree()
            for d in testdata:
                t.add_node(TestNode(d))
            return t
        
        def validate_reinsertion(node, new_value, replacement_value, replacement_position):
            self.assertIsNotNone(node, 'new node should be reinserted into the right position')
            self.assertEqual(node.value(), new_value, 'new node should have been inserted')
            self.assertEqual(replacement_position.value(), replacement_value, 'node should have been replaced with the correct value')

        def perform_validated_reinsert(tr, new_node, new_value, replacement_value, original_node):
            on = original_node(tr)
            on.v = new_value
            tr.reinsert_node(on)
            validate_reinsertion(new_node(tr), new_value, replacement_value, original_node(tr))
            print('new tree:')
            print(tr)

        tc = build_test_tree()

        """
        1005344
            137029

            1972421
                1937498
                    1925201
        """

        perform_validated_reinsert(tc, lambda tr: tr.root.left.right, 996576, 1925201, lambda tr: tr.root)
        
        """
        1925201
            137029
                None

                996576

            1972421
                1937498
        """

        perform_validated_reinsert(tc, lambda tr: tr.root.right.right, 1989604, 1937498, lambda tr: tr.root.right)

    def test_reinsertion_2(self):
        """
        tree:
        root: 1697105
                left: 384151
                        left: 318798
                                left: 22284
                                        left: None
                                        right: None
                                right: None
                        right: 1604855
                                left: None
                                right: None
                right: None
        updating: 384151
        new node value: 386628
        updating: 318798
        new node value: 310955
        updating: 22284
        new node value: 19588
        updating: 1697105
        new node value: 1671160
        updating: 1604855
        new node value: 1614889
        tree:
        root: 1671160
                left: 1614889
                        left: None
                        right: None
                right: None
        """
        testdata = [1697105, 384151, 318798, 22284, 1604855]

        def build_test_tree() -> BinaryTree:
            t = BinaryTree()
            for d in testdata:
                t.add_node(TestNode(d))
            return t
        
        def validate_reinsertion(node, new_value, replacement_value, replacement_position):
            self.assertIsNotNone(node, 'new node should be reinserted into the right position')
            self.assertEqual(node.value(), new_value, 'new node should have been inserted')
            self.assertEqual(replacement_position.value(), replacement_value, 'node should have been replaced with the correct value')

        def perform_validated_reinsert(tr, new_node, new_value, replacement_value, original_node):
            on = original_node(tr)
            on.v = new_value
            tr.reinsert_node(on)
            validate_reinsertion(new_node(tr), new_value, replacement_value, original_node(tr))
            print('new tree:')
            print(tr)

        tc = build_test_tree()

        print(tc)

        """
        1697105
            384151
                318798
                    22284

                1604855
        """

        perform_validated_reinsert(tc, lambda tr: tr.root.left.left.right, 386628, 1604855, lambda tr: tr.root.left)
        
        """
        1697105
            1604855
                318798
                    22284

                    386628
        """

        perform_validated_reinsert(tc, lambda tr: tr.root.left.left.left.right, 310955, 386628, lambda tr: tr.root.left.left)
        
        """
        1697105
            1604855
                386628
                    22284
                        None

                        310955
        """

        perform_validated_reinsert(tc, lambda tr: tr.root.left.left.left.left, 19588, 310955, lambda tr: tr.root.left.left.left)
        
        """
        1697105
            1604855
                386628
                    310955
                        19588
        """

        perform_validated_reinsert(tc, lambda tr: tr.root.right, 1671160, 1604855, lambda tr: tr.root)
        
        """
        1604855
            386628
                310955
                    19588

            1671160
        """

        perform_validated_reinsert(tc, lambda tr: tr.root.left.right, 1614889, 1671160, lambda tr: tr.root)
        
        """
        1671160
            386628
                310955
                    19588

                1614889
        """

    def test_reinsertion_3(self):
        """
        tree:
        root: 255020
            left: 130863
                left: 1832
                    left: None
                    right: None
                right: None
            right: 379689
                left: None
                right: 422731
                    left: None
                    right: None
        updating: 255020
        new node value: 256618
        updating: 130863
        new node value: 2377867
        updating: 379689
        new node value: 390544
        updating: 1832
        new node value: 641253
        updating: 422731
        new node value: 431078
        """
        testdata = [255020, 130863, 1832, 379689, 422731]

        def build_test_tree() -> BinaryTree:
            t = BinaryTree()
            for d in testdata:
                t.add_node(TestNode(d))
            return t
        
        def validate_reinsertion(node, new_value, replacement_value, replacement_position):
            self.assertIsNotNone(node, 'new node should be reinserted into the right position')
            self.assertEqual(node.value(), new_value, 'new node should have been inserted')
            self.assertEqual(replacement_position.value(), replacement_value, 'node should have been replaced with the correct value')

        def perform_validated_reinsert(tr, new_node, new_value, replacement_value, original_node):
            on = original_node(tr)
            on.v = new_value
            tr.reinsert_node(on)
            validate_reinsertion(new_node(tr), new_value, replacement_value, original_node(tr))
            print('new tree:')
            print(tr)

        tc = build_test_tree()

        print(tc)

        """
        255020
            130863
                1832

            379689
                None

                422731
        """

        perform_validated_reinsert(tc, lambda tr: tr.root.left.right, 255618, 379689, lambda tr: tr.root)

        """
        379689
            130863
                1832

                255618

            422731
        """

        perform_validated_reinsert(tc, lambda tr: tr.root.right.right, 2377867, 255618, lambda tr: tr.root.left)

