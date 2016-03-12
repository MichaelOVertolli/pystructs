import unittest
from pystructs.trees.binarytree import BinTree, NoMiddleException, EqualityException
from random import shuffle

#python -m unittest discover \\\from Data_structures

class GetMiddleIndexTest(unittest.TestCase):

    def setUp(self):
        self.t = BinTree([])

    def test_balanced(self):
        self.assertEqual(self.t.getmiddleindex(0, 3), 1)

    def test_unbalanced(self):
        self.assertEqual(self.t.getmiddleindex(0, 2), 1)

    def test_slice_balanced(self):
        self.assertEqual(self.t.getmiddleindex(8, 15), 11)

    def test_slice_unbalanced(self):
        self.assertEqual(self.t.getmiddleindex(8, 14), 11)

    def test_input_error_bot(self):
        self.assertRaises(TypeError, self.t.getmiddleindex, '5', 5)

    def test_input_error_top(self):
        self.assertRaises(TypeError, self.t.getmiddleindex, 5, '5')

    def test_nomiddleexception(self):
        self.assertRaises(NoMiddleException, self.t.getmiddleindex, 5, 6)

    def test_equalityexception(self):
        self.assertRaises(EqualityException, self.t.getmiddleindex, 5, 5)

    def test_valueerror(self):
        self.assertRaises(ValueError, self.t.getmiddleindex, 6, 5)


class BinTreeTest(unittest.TestCase):

    def setUp(self):
        self.iterable = range(13)

    def test_zero_init(self):
        t = BinTree([])
        self.assertIsNone(t.tree)

    def test_one_init(self):
        t = BinTree([0])
        self.assertDictEqual(t.tree, 
                             {'root': 0,
                              0: [None, None, None]})

    def test_balanced_init(self):
        t = BinTree(self.iterable[0:3], True)
        self.assertDictEqual(t.tree, 
                             {'root': 1, 
                              1: [None, 0, 2], 
                              0: [1, None, None], 
                              2: [1, None, None]})

    def test_unbalanced_init(self):
        t = BinTree(self.iterable[0:2], True)
        self.assertDictEqual(t.tree,
                             {'root': 1,
                              1: [None, 0, None],
                              0: [1, None, None]})

    def test_large_init(self):
        t = BinTree(self.iterable, True)
        self.assertDictEqual(t.tree,
                             {'root': 6,
                              6: [None, 3, 10],
                              3: [6, 1, 5],
                              1: [3, 0, 2],
                              0: [1, None, None],
                              2: [1, None, None],
                              5: [3, 4, None],
                              4: [5, None, None],
                              10: [6, 8, 12],
                              8: [10, 7, 9],
                              7: [8, None, None],
                              9: [8, None, None],
                              12: [10, 11, None],
                              11: [12, None, None]})

    def test_sort_large_init(self):
        shuffle(self.iterable)
        t = BinTree(self.iterable, False)
        self.assertDictEqual(t.tree,
                             {'root': 6,
                              6: [None, 3, 10],
                              3: [6, 1, 5],
                              1: [3, 0, 2],
                              0: [1, None, None],
                              2: [1, None, None],
                              5: [3, 4, None],
                              4: [5, None, None],
                              10: [6, 8, 12],
                              8: [10, 7, 9],
                              7: [8, None, None],
                              9: [8, None, None],
                              12: [10, 11, None],
                              11: [12, None, None]})

    def test_get_first(self):
        t = BinTree(self.iterable, True)
        self.assertEqual(t.get_first(), 0)

    def test_get_last(self):
        t = BinTree(self.iterable, True)
        self.assertEqual(t.get_last(), 12)