import warnings
from collections import deque
from math import log
from random import random


class BinTree(object):

    PARENT = 0
    LEFT = 1
    RIGHT = 2

    def getmiddleindex(self, bot, top):
        """Returns middle index between [bot, top)."""
        if type(bot) is not int or type(top) is not int:
            raise TypeError('Invalid input. Both values must be int.')
        if top - bot < 0:
            raise ValueError(
                "Invalid input combination. bot and top are incorrectly" +
                "ordered.")
        elif top == bot:
            raise EqualityException('Invalid input. The two values are equal.')
        elif top - bot == 1:
            raise NoMiddleException(
                'Invalid input. There is no middle value between ' + str(
                    bot) + ' and ' + str(top))
        return (bot + top) / 2

    def setmiddleindex(self, lower, upper, assign, stack):
        # not used right now.
        try:
            # I do not like this call
            mid = self.getmiddleindex(lower, upper)
        except NoMiddleException:
            mid = assign
        except EqualityException:
            # This should never happen.
            warnings.warn('Unexpected equality in left segment for values: ' +
                          str((lower, mid, upper)))
            mid = None
        else:
            stack.append((lower, mid, upper))
        return mid

    def __init__(self, iterable, sorted_=False):
        """Makes a balanced binary tree from an iterable with no duplicates.

        """
        len_ = len(iterable)
        if len(set(iterable)) < len_:
            raise DuplicateException(
                'Bintree assumes you are handling duplicates separately.')
        if len_ == 0:
            bintree = {'root': None}
        elif len_ == 1:
            bintree = {iterable[0]: [None, None, None], 'root': iterable[0]}
        else:
            if not sorted_:
                iterable = sorted(iterable)
            try:
                bintree = {key: [None, None, None] for key in iterable}
            except TypeError as e:
                raise TypeError('All values in a BinTree must be hashable.' +
                                ' At least one value is not hashable. ' +
                                str(e))
            # Assuming the tree is balanced, then the maximum breadth is
            # the level (or log of size) that is not partial and the size
            # of that level is 2**level
            stack = deque(maxlen=2**int(log(len_, 2)))
            getmiddleindex = self.getmiddleindex
            root = getmiddleindex(0, len_)
            bintree['root'] = root
            stack.append((0, root, len_))
            PARENT = BinTree.PARENT
            LEFT = BinTree.LEFT
            RIGHT = BinTree.RIGHT
            while len(stack) > 0:
                bot, mid, top = stack.pop()
                # Two checks to see if the child nodes are leaves
                try:
                    l_mid = getmiddleindex(bot, mid)
                except NoMiddleException:
                    l_mid = bot
                except EqualityException:
                    # This should never happen.
                    warnings.warn('Unexpected equality in left segment for' +
                                  'values: ' + str((bot, mid, top)))
                    l_mid = None
                else:
                    stack.append((bot, l_mid, mid))
                try:
                    r_mid = getmiddleindex(mid + 1, top)
                except NoMiddleException:
                    r_mid = top - 1
                except EqualityException:
                    r_mid = None
                else:
                    stack.append((mid + 1, r_mid, top))
                # sets leaves in tree
                bintree[iterable[mid]][LEFT] = l_mid
                bintree[iterable[mid]][RIGHT] = r_mid
                # sets parents in tree
                try:
                    l_val = iterable[l_mid]
                except TypeError:
                    pass
                else:
                    bintree[l_val][PARENT] = mid
                try:
                    r_val = iterable[r_mid]
                except TypeError:
                    pass
                else:
                    bintree[r_val][PARENT] = mid
        self.tree = bintree

    def get_loop(self, dir_, start):
        t = self.tree
        if start == 'root':
            node = t[start]
        else:
            node = start
        while t[node][dir_] is not None:
            node = t[node][dir_]
        return node

    def get_first(self):
        return self.get_loop(self.LEFT, 'root')

    def get_last(self):
        return self.get_loop(self.RIGHT, 'root')

    def get_root(self):
        return self.tree['root']

    def find(self, val):
        try:
            node = self.tree[val]
        except KeyError:
            node = None
        return node

    def insert(self, val):
        t = self.tree
        try:
            t[val]
        except KeyError:
            t[val] = [None, None, None]
        else:
            raise DuplicateException(
                'Invalid input to insert. Bintree assumes you' +
                'are handling duplicates separately.')
        PARENT = BinTree.PARENT
        LEFT = BinTree.LEFT
        RIGHT = BinTree.RIGHT
        dir_ = None
        parent = 'root'
        node = t['root']
        while node is not None:
            if val < node:
                dir_ = LEFT
            else:
                dir_ = RIGHT
            parent = node
            node = t[node][dir_]
        if dir_ is None:
            t[parent] = val
        else:
            t[parent][dir_] = val
            t[val][PARENT] = parent

    def delete(self, val, rand=random):
        """Deletes val from the binary tree.

        Raises a warning if the value doesn't exist.

        val := (any type) the value to delete
        rand := (func) special testing function to specify random
                       aspects of the function.

        """

        t = self.tree
        try:
            node = t[val]
        except KeyError:
            warnings.warn('No value deleted. ' + str(val) + ' not in tree.')
        else:
            PARENT = BinTree.PARENT
            LEFT = BinTree.LEFT
            RIGHT = BinTree.RIGHT
            parent = node[PARENT]
            parentnode = t[parent]
            if parentnode[LEFT] == val:
                loc = LEFT
            else:
                loc = RIGHT
            if node[LEFT] is None:
                if node[RIGHT] is None:
                    new_node = None
                else:
                    new_node = node[RIGHT]
            else:
                if node[RIGHT] is None:
                    new_node = node[LEFT]
                else:
                    # prevents degeneration caused by regularly picking
                    # the same side
                    if rand() > 0.5:
                        # (direction, start_node)
                        dir_ = (LEFT, node[RIGHT])
                    else:
                        dir_ = (RIGHT, node[LEFT])
                    new_node = self.get_loop(*dir_)
                    self.delete(new_node)
                    t[new_node] = node
                    # only happens if both nodes exist
                    # don't need to check
                    t[node[LEFT]][PARENT] = new_node
                    t[node[RIGHT]][PARENT] = new_node
            parentnode[loc] = new_node
            try:
                temp = t[new_node]
            except KeyError:
                pass
            else:
                temp[PARENT] = parent
            del t[val]


class DuplicateException(Exception):
    """Occurs if there are any duplicates in the iterable."""
    pass


class NoMiddleException(Exception):
    """
    pass


class EqualityException(Exception):
    pass
