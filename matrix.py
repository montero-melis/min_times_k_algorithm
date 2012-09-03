#!/usr/bin/env python2

class SquareMatrix:
    def __init__(self,n,**kwargs):
        # Get keyword arguments
        identity = kwargs.get('identity')

        # square matrix of size n x n
        self.n = n

        self.data = []
        for i in range(n):
            row = [0]*n
            if identity:
                row[i] = 1
            self.data.append(row)

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

