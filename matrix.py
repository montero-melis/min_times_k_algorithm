#!/usr/bin/env python2

import itertools

class Matrix:
    def __init__(self,nr=None,nc=None):
        if nr:
            if not nc:
                nc = nr

            self.rows = []
            for i in xrange(nr):
                row = [0]*nc
                self.rows.append(row)
        else:
            self.rows=[[]]

        self.setdim()

    @classmethod
    def build(cls,lst):
        m = Matrix()
        m.rows = lst
        m.setdim()
        return m
   
    @classmethod
    def identity(cls,nr):
        m = Matrix(nr)
        for i in range(nr):
            m[i,i] = 1
        return m

    @classmethod
    def pairs(cls,set,nr=None):
        if not nr:
            nr = len(set)
        m = Matrix(nr)
        for pair in itertools.combinations_with_replacement(set,2):
            m[pair] = 1
        return m

    def setdim(self):
        self.nr = len(self.rows)
        self.nc = len(self.rows[0])

    def transpose(self):
        return Matrix.build(zip(*self.rows))

    def __add__(self,other):
        m = Matrix(self.nr,self.nc)

        for i in xrange(self.nr):
            for j in xrange(self.nc):
                m[i,j] = self[i,j] + other[i,j]

        return m

    def __sub__(self,other):
        m = Matrix(self.nr,self.nc)

        for i in xrange(self.nr):
            for j in xrange(self.nc):
                m[i,j] = self[i,j] - other[i,j]

        return m

    def __setitem__(self,k,v):
        i,j = k
        self.rows[i][j] = v

    def __getitem__(self,k):
        i,j = k
        return self.rows[i][j]

    def __str__(self):
        render = '['
        for i in xrange(self.nr):
            if i > 0:
                render += ' ['
            else:
                render += '['

            row = []
            for j in xrange(self.nc):
                col_w = max([len(str(e)) for e in self.col(j)])
                row.append(str(self[i,j]).rjust(col_w))
            render += ', '.join(row) + "]"
            if i < self.nr-1:
                render += ",\n"

        render += ']'
        return render

    def row(self,i):
        return self.rows[i]

    def col(self,j):
        return [row[j] for row in self.rows]

    def swap_row(self,i, j):
        m = Matrix.build(self.rows)
        m.rows[i],m.rows[j] = self.rows[j],self.rows[i]
        return m

    def swap_col(self,i,j):
        m = Matrix.build(self.rows)
        m = m.transpose()
        m = m.swap_row(i,j)
        return m.transpose()
