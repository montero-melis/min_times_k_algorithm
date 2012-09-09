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
            # print "\n--- loop %i ---" % (self.safe_exit,)
            self.safe_exit += 1

            next_j = self.find_pair()
            # print ["next_j",next_j]

            if next_j != None:
                self.assign_j(next_j)

            if self.finished():
                break

            if next_j != None:
                self.i = self.j
            else:
                next_i = self.find_next()
                self.assign_i(next_i)
                if self.finished():
                        break

            # print self.results.r()

        # print "--- END ---"
        # print "r      ",self.results.r()
        # print "column ",self.results.column
        # print "subsets",self.results.subsets

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
        col_complete = self.results.column_complete()
        all_pairs    = self.adjacency_matrix().all_pairs()

        if self.safe_exit > 2000 or (col_complete and all_pairs):
            print "==== END ===="
            print ["col_complete",col_complete]
            print ["all_pairs", all_pairs]
            print ["safe_exit", self.safe_exit]
            print
            return True
        else:
            return False

if __name__ == "__main__":
    n,k = map(int,sys.argv[1:])

    min_t_k = MinTimesK(n,k)
    min_t_k.solve()


    r = min_t_k.results.subsets

    print r

    # check the result
    l = set(itertools.combinations(range(n),2))

    for group in r:
        group_int = [ int(i) for i in sorted(group)]
        group_set = set(itertools.combinations(group_int,2))
        l = l - group_set

    if len(l) == 0:
        print "correct"
    else:
        print "missing pairs:"
        print l

    #print M.pairs(r,n)


