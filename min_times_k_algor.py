#!/usr/bin/env python

import sys
import itertools
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
        return len(self.column) % self.K == 0
        # return len(self.column) == 0

    def r(self):
        r = self.subsets[:]
        if self.column:
            r.append(self.column)
        return r

    def min_times_k(self):
        return len(self.subsets)

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

    def solve(self):
        self.assign_i(self.find_next())

        while True:
            if self.results.column_complete():
                next_i = self.find_next()
                self.assign_i(next_i)

            next_j = self.find_pair()

            if next_j != None:
                self.assign_j(next_j)
                self.i = self.j
            else:
                next_i = self.find_next()
                self.assign_i(next_i)

            if self.finished(): break

    def assign_i(self,i):
        self.i = i
        self.results.append(i)

    def assign_j(self,j):
        self.j = j
        self.results.append(j)

    def adjacency_matrix(self):
        return M.pairs(self.results.r(),self.N)

    def find_next(self):
        return self.adjacency_matrix().find_next(self.results.r())

    def find_pair(self):
        return self.adjacency_matrix().find_pair(self.results.r())

    def finished(self):
        col_complete = self.results.column_complete()
        all_pairs    = self.adjacency_matrix().all_pairs()

        if col_complete and all_pairs:
            return True
        else:
            return False

if __name__ == "__main__":
    if len(sys.argv[1:]) == 2:
        # accept command line args
        n,k = map(int,sys.argv[1:])
    else:
        # otherwise use hardcoded args
        n = 20
        k = 6

    min_t_k = MinTimesK(n,k)
    min_t_k.solve()

    r = min_t_k.results.subsets

    print "Subsets:"
    print M.build(r)
    print

    print "Pairs:"
    m_pairs = M.pairs(r,n)
    max_num = 0
    for i,row in enumerate(m_pairs.rows):
        val = max(i,max(row))
        max_num = max(max_num, len(str(val)))

    for i,row in enumerate(m_pairs.rows):
        print "%s: %s" % (str(i).rjust(max_num), str(row[:(i+1)]).ljust(max_num))
    print

    print "min_times_k = %i" % min_t_k.results.min_times_k()

    # check the result
    missing = []
    for i in xrange(n):
        for j in xrange(n):
            if i == j: continue
            if m_pairs[i,j] == 0:
                missing.append([i,j])

    print
    if len(missing) == 0:
        print "CORRECT"
    else:
        print "Missing pairs:"
        print missing

