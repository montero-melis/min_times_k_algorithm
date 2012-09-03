#!/usr/bin/env python2

import itertools

class SquareMatrix:
    def __init__(self,builder,**kwargs):
        # Get keyword arguments
        identity = kwargs.get('identity')

        if isinstance(builder,list):
            self.data = builder
            self.n    = len(builder)
        else:
            self.n = builder

            self.data = []
            for i in range(self.n):
                row = [0]*self.n
                if identity:
                    row[i] = 1
                self.data.append(row)

    @classmethod
    def identity(cls,n):
        return SquareMatrix(n, identity = True)

    @classmethod
    def pairs(cls,n,set):
        m = SquareMatrix(n)
        for pair in itertools.combinations(set,2):
            m[pair] = 1
        return m

    def __add__(self,other):
        m = SquareMatrix(self.n)

        for i in xrange(self.n):
            for j in xrange(self.n):
                m[i,j] = self[i,j] + other[i,j]

        return m

    def __sub__(self,other):
        m = SquareMatrix(self.n)


        for i in xrange(self.n):
            for j in xrange(self.n):
                m[i,j] = self[i,j] - other[i,j]

        return m

    def __setitem__(self,k,v):
        i,j = k
        self.data[i][j] = v

    def __getitem__(self,k):
        i,j = k
        return self.data[i][j]

    def __str__(self):
        render = '['
        for i in range(self.n):
            if i > 0:
                render += ' ['
            else:
                render += '['

            row = []
            for j in range(self.n):
                col_w = max([len(str(e)) for e in self.col(j)])
                row.append(str(self[i,j]).rjust(col_w))
            render += ', '.join(row) + "]"
            if i < self.n-1:
                render += ",\n"

        render += ']'
        return render

    def row(self,i):
        return self.data[i]

    def col(self,j):
        return [x[j] for x in self.data]

