from cProfile import runctx
from timeit import Timer
from pystructs.trees.binarytree import BinTree
from random import sample
from bintrees import BinaryTree
from sys import argv

# python -m pystructs.profiling.profile_binarytree.py

COUNT = 100
KEYS = 5000
KEYRANGE = 1000000

setup_BinTree_timer = """
from __main__ import bintree_build
"""


def random_keys():
    return sample(range(KEYRANGE), KEYS)


keys = random_keys()


def bintree_build():
    BinTree(keys, sorted_=True)


def bintree_build2():
    BinaryTree.from_keys(keys)


def print_result(time, text):
    print "Operation: {} takes {:.2f} seconds\n".format(text, time)


def main_timer():
    t = Timer("bintree_build()", setup_BinTree_timer)
    print_result(t.timeit(COUNT), 'BinaryTree build only.')


def main_profile():
    runctx('bintree_build()', {'keys': keys,
                               'bintree_build': bintree_build}, {})
    runctx('bintree_build2()', {'keys': keys,
                                'bintree_build2': bintree_build2}, {})


if __name__ == '__main__':
    arg = argv[1]
    if arg == 't':
        main_timer()
    elif arg == 'p':
        main_profile()
    elif arg == 'h':
        print '***HELP***'
        print 't flag runs timer profiling'
        print 'p flag runs cProfile profiling'
        print '**********'
    else:
        print 'Not a valid option.'
