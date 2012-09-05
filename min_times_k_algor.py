#!/usr/bin/env python

import sys
from matrix import MinTimesKMatrix as M

class Results:
    def __init__(self,n,k):
        self.N = n
        self.K = k
        self.column  = []
        self.subsets = []

    def append(self, value):
        self.column.append(value)
        if self.column_complete():
            column_copy = self.column
            self.subsets.append(column_copy)
            self.column = []

    def column_complete(self):
        # return len(self.column) % self.K == 0
        return len(self.column) == self.K

    def r(self):
        if self.subsets:
            r = self.subsets
        else:
            r = []
        if self.column:
            r.append(self.column)
        return r

class MinTimesK:
    """
    This is the class used to calculate the minimum number of ...
    Willy, a bit of literature here, s'il te plait !

    Instance variables:

        self.N:

        self.K:

        self.i:
            The current i-index.

        self.j:
            The current j-index.
    """

    def __init__(self, n, k):
        """
        Initializes all the instance variables.

        Arguments:
            n: The number of elements in the sample.
            k: The size of the experiment groups.
        """

        self.N = n
        self.K = k

        self.i = None
        self.j = None

        self.results          = Results(self.N,self.K)
        #self.adjacency_matrix = M(self.N)

        self.safe_exit = 0 # Just for debugging


    def debug(self,label):
        i = self.i
        j = self.j

        print "[%s] i=%s, j=%s" % (label,str(i),str(j))

    def solve(self):
        self.i = self.find_next()
        self.results.append(self.i)

        # while not self.finished():
        for kk in range(4):

            # print "--- %i" % (kk)
            # self.debug("uno")

            self.j = self.find_pair()
            self.results.append(self.j)

            # self.debug("dos")

            if self.j:
                # self.debug("tres")
                self.i = self.j
            else:
                self.i = self.find_next()
                self.results.append(self.i)


            # self.debug("cuatro")

        print "---"
        print "r      ",self.results.r()
        print "column ",self.results.column
        print "subsets",self.results.subsets

        # wtf
        self.results.subsets[1][0] = 7
        print "subsets",self.results.subsets

    def adjacency_matrix(self):
        return M.pairs(self.results.r(),self.N)

    def find_next(self):
        if not self.i:
            return 0
        else:
            return self.adjacency_matrix().find_next()

    def find_pair(self):
        return self.adjacency_matrix().find_pair(self.results.r())

    def finished(self):
        self.safe_exit += 1

        col_complete = self.results.column_complete()
        all_pairs    = self.adjacency_matrix().all_pairs()

        if self.safe_exit > 10 or (col_complete and all_pairs):
            print self.results.subsets
            return True
        else:
            return False

min_t_k = MinTimesK(5,3)
min_t_k.solve()
