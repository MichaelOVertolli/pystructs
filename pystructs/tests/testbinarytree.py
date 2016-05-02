import unittest
import warnings
from mock import patch
from random import shuffle

from pystructs.trees.binarytree import (BinTree, EqualityException,
                                        NoMiddleException, DuplicateException)


# python -m unittest discover \\\from Data_structures

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

    def test_duplicate_init(self):
        self.assertRaises(DuplicateException, BinTree, [5, 5])

    def test_zero_init(self):
        t = BinTree([])
        self.assertIsNone(t.tree['root'])

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

    def test_get_loop(self):
        t = BinTree(self.iterable, True)
        self.assertEqual(t.get_loop(BinTree.LEFT, 10), 7)

    def test_get_loop_ValueError(self):
        t = BinTree(self.iterable, True)
        self.assertRaises(ValueError, t.get_loop, BinTree.LEFT, 50)

    def test_get_first(self):
        t = BinTree(self.iterable, True)
        self.assertEqual(t.get_first(), 0)

    def test_get_last(self):
        t = BinTree(self.iterable, True)
        self.assertEqual(t.get_last(), 12)

    def test_find_success(self):
        t = BinTree(self.iterable, True)
        self.assertSequenceEqual(t.find(5), [3, 4, None])

    def test_find_fail(self):
        t = BinTree(self.iterable, True)
        self.assertIsNone(t.find(50))

    @patch.object(warnings, 'warn')
    def test_delete_UserWarning(self, mock_warn):
        t = BinTree(self.iterable, True)
        t.delete(50)
        self.assertTrue(mock_warn.called)

    def test_delete_no_children(self):
        t = BinTree(self.iterable, True)
        t.delete(2)
        self.assertDictEqual(t.tree,
                             {'root': 6,
                              6: [None, 3, 10],
                              3: [6, 1, 5],
                              1: [3, 0, None],
                              0: [1, None, None],
                              5: [3, 4, None],
                              4: [5, None, None],
                              10: [6, 8, 12],
                              8: [10, 7, 9],
                              7: [8, None, None],
                              9: [8, None, None],
                              12: [10, 11, None],
                              11: [12, None, None]})

    def test_delete_left_child(self):
        t = BinTree(self.iterable, True)
        t.delete(5)
        self.assertDictEqual(t.tree,
                             {'root': 6,
                              6: [None, 3, 10],
                              3: [6, 1, 4],
                              1: [3, 0, 2],
                              0: [1, None, None],
                              2: [1, None, None],
                              4: [3, None, None],
                              10: [6, 8, 12],
                              8: [10, 7, 9],
                              7: [8, None, None],
                              9: [8, None, None],
                              12: [10, 11, None],
                              11: [12, None, None]})

    def test_delete_right_child(self):
        t = BinTree(self.iterable, True)
        t.delete(7)
        t.delete(8)
        self.assertDictEqual(t.tree,
                             {'root': 6,
                              6: [None, 3, 10],
                              3: [6, 1, 5],
                              1: [3, 0, 2],
                              0: [1, None, None],
                              2: [1, None, None],
                              5: [3, 4, None],
                              4: [5, None, None],
                              10: [6, 9, 12],
                              9: [10, None, None],
                              12: [10, 11, None],
                              11: [12, None, None]})

    def test_delete_both_childs_rightrand(self):
        t = BinTree(self.iterable, True)
        # forces random check to always pass

        def dump():
            return 0.7
        t.delete(10, dump)
        self.assertDictEqual(t.tree,
                             {'root': 6,
                              6: [None, 3, 11],
                              3: [6, 1, 5],
                              1: [3, 0, 2],
                              0: [1, None, None],
                              2: [1, None, None],
                              5: [3, 4, None],
                              4: [5, None, None],
                              11: [6, 8, 12],
                              8: [11, 7, 9],
                              7: [8, None, None],
                              9: [8, None, None],
                              12: [11, None, None]})

    def test_delete_both_childs_leftrand(self):
        t = BinTree(self.iterable, True)
        # forces random check to always pass

        def dump():
            return 0.4
        t.delete(10, dump)
        self.assertDictEqual(t.tree,
                             {'root': 6,
                              6: [None, 3, 9],
                              3: [6, 1, 5],
                              1: [3, 0, 2],
                              0: [1, None, None],
                              2: [1, None, None],
                              5: [3, 4, None],
                              4: [5, None, None],
                              9: [6, 8, 12],
                              8: [9, 7, None],
                              7: [8, None, None],
                              12: [9, 11, None],
                              11: [12, None, None]})

    def test_delete_both_childs_root(self):
        t = BinTree(self.iterable, True)
        # forces random check to always pass

        def dump():
            return 0.7
        t.delete(6, dump)
        self.assertDictEqual(t.tree,
                             {'root': 7,
                              7: [None, 3, 10],
                              3: [7, 1, 5],
                              1: [3, 0, 2],
                              0: [1, None, None],
                              2: [1, None, None],
                              5: [3, 4, None],
                              4: [5, None, None],
                              10: [7, 8, 12],
                              8: [10, None, 9],
                              9: [8, None, None],
                              12: [10, 11, None],
                              11: [12, None, None]})

    def test_insert_DuplicateException(self):
        t = BinTree(self.iterable, True)
        self.assertRaises(DuplicateException, t.insert, 3)

    def test_insert_root(self):
        t = BinTree([], True)
        t.insert(5)
        self.assertDictEqual(t.tree, {5: [None, None, None],
                                      'root': 5})

    def test_insert_right(self):
        t = BinTree(self.iterable, True)
        t.insert(13)
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
                              12: [10, 11, 13],
                              11: [12, None, None],
                              13: [12, None, None]})

    def test_insert_left(self):
        t = BinTree(self.iterable, True)
        t.delete(4)
        t.insert(4)
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
