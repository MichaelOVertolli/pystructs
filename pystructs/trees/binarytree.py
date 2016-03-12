from collections import deque
from math import log
from warnings import warn

class BinTree(object):

    PARENT = 0
    LEFT = 1
    RIGHT = 2

    def getmiddleindex(self, bot, top):
        """Returns middle index between [bot, top)."""
        if type(bot) is not int or type(top) is not int:
            raise TypeError('Invalid input. Both values must be int.')
        if top-bot < 0:
            raise ValueError('Invalid input combination. bot and top are incorrectly ordered.')
        elif top == bot:
            raise EqualityException('Invalid input. The two values are equal.')
        elif top-bot == 1:
            raise NoMiddleException('Invalid input. There is no middle value between ' + str(bot) + ' and ' + str(top))
        return (bot+top)/2

    def setmiddleindex(self, lower, upper, assign, stack):
        #not used right now.
        try:
            #I do not like this call
            mid = self.getmiddleindex(lower, upper)
        except NoMiddleException:
            mid = assign
        except EqualityException:
            #This should never happen.
            warn('Unexpected equality in left segment for values: '+str((lower, mid, upper)))
            mid = None
        else:
            stack.append((lower, mid, upper))
        return mid

    def __init__(self, iterable, sorted_=False):
        """Makes a balanced binary tree from an iterable with no duplicates.

        """
        len_ = len(iterable)
        if len(set(iterable)) < len_:
            raise DuplicateException('Bintree assumes you are handling duplicates separately.')
        #add duck type check to see that eq, lt, gt are implemented.
        if len_ == 0:
            bintree = None
        elif len_ == 1:
            bintree = {iterable[0]: [None, None, None], 'root': iterable[0]}
        else:
            if not sorted_:
                iterable = sorted(iterable)
            bintree = {key: [None, None, None] for key in iterable}
            #Assuming the tree is balanced, then the maximum breadth is
            #the level (or log of size) that is not partial and the size
            #of that level is 2**level
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
                #Two checks to see if the child nodes are leaves
                try:
                    l_mid = getmiddleindex(bot, mid)
                except NoMiddleException:
                    l_mid = bot
                except EqualityException:
                    #This should never happen.
                    warn('Unexpected equality in left segment for values: '+str((bot, mid, top)))
                    l_mid = None
                else:
                    stack.append((bot, l_mid, mid))
                try:
                    r_mid = getmiddleindex(mid+1, top)
                except NoMiddleException:
                    r_mid = top-1
                except EqualityException:
                    r_mid = None
                else:
                    stack.append((mid+1, r_mid, top))
                #sets leaves in tree
                bintree[iterable[mid]][LEFT] = l_mid
                bintree[iterable[mid]][RIGHT] = r_mid
                #sets parents in tree
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

    def get_loop(self, dir):
        t = self.tree
        node = t['root']
        while t[node][dir] is not None:
            node = t[node][dir]
        return node

    def get_first(self):
        return self.get_loop(self.LEFT)

    def get_last(self):
        return self.get_loop(self.RIGHT)

class DuplicateException(Exception):
    pass

class NoMiddleException(Exception):
    pass

class EqualityException(Exception):
    pass
