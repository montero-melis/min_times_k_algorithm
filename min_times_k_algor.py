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
        r = self.subsets[:]
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

        self.i = 0
        self.j = 0

        self.results          = Results(self.N,self.K)
        #self.adjacency_matrix = M(self.N)

        self.safe_exit = 0 # Just for debugging


    def debug(self,label):
        i = self.i
        j = self.j
        print "[%s] i=%s, j=%s" % (label,str(i),str(j))

    def solve(self):
        self.assign_i(self.find_next())

        while True:
            print "\n--- loop %i ---" % (self.safe_exit,)
            self.assign_j(self.find_pair())
            if self.finished():
                break

            if self.j != None:
                self.j_to_i()
            else:
                self.assign_i(self.find_next())
                if self.finished():
                    break

            print self.results.r()

        print "--- END ---"
        print "r      ",self.results.r()
        print "column ",self.results.column
        print "subsets",self.results.subsets

    def j_to_i(self):
        # print "i=j=%i" % (self.j)
        j = self.j
        self.i = j

    def assign_i(self,i):
        # print "assign_i: %s" % (str(i),)
        self.i = i
        self.results.append(i)

    def assign_j(self,j):
        # print "assign_j: %s" % (str(j),)
        self.j = j
        self.results.append(j)

    def adjacency_matrix(self):
        return M.pairs(self.results.r(),self.N)

    def find_next(self):
        return self.adjacency_matrix().find_next()

    def find_pair(self):
        return self.adjacency_matrix().find_pair(self.results.r())

    def finished(self):
        self.safe_exit += 1

        col_complete = self.results.column_complete()
        all_pairs    = self.adjacency_matrix().all_pairs()

        if self.safe_exit > 20 or (col_complete and all_pairs):
            return True
        else:
            return False


min_t_k = MinTimesK(5,3)
min_t_k.solve()
