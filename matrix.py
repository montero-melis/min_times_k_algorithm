#!/usr/bin/env python2

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
        m = cls()
        m.rows = lst
        m.setdim()
        return m

    @classmethod
    def identity(cls,nr):
        m = cls(nr)
        for i in range(nr):
            m[i,i] = 1
        return m

    def setdim(self):
        self.nr = len(self.rows)
        self.nc = len(self.rows[0])

    def transpose(self):
        return self.__class__.build(zip(*self.rows))

    def __add__(self,other):
        m = self.__class__(self.nr,self.nc)

        for i in xrange(self.nr):
            for j in xrange(self.nc):
                m[i,j] = self[i,j] + other[i,j]

        return m

    def __sub__(self,other):
        m = self.__class__(self.nr,self.nc)

        for i in xrange(self.nr):
            for j in xrange(self.nc):
                m[i,j] = self[i,j] - other[i,j]

        return m

    def __mul__(self,other):
        m = self.__class__(self.nr,other.nc)
        for i in range(self.nr):
            for j in range(other.nc):
                for k in range(other.nr):
                    m[i,j] += self[i,k]*other[k,j]
        return m

    def __setitem__(self,k,v):
        i,j = k
        self.rows[i][j] = v

    def __getitem__(self,k):
        i,j = k
        try:
            value = self.rows[i][j]
        except IndexError:
            value = 0
        return value

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
        m = self.__class__.build(self.rows)
        m.rows[i],m.rows[j] = self.rows[j],self.rows[i]
        return m

    def swap_col(self,i,j):
        m = self.__class__.build(self.rows)
        m = m.transpose()
        m = m.swap_row(i,j)
        return m.transpose()

    def diagonal(self,offset=0):
        diagonal_list = []
        for i in xrange(self.nr):
            if offset >= 0:
                if i+offset >= self.nr:
                    break
                diagonal_list.append(self[i,i+offset])
            else:
                if i-offset >= self.nc:
                    break
                diagonal_list.append(self[i-offset,i])
        return diagonal_list

    def clone(self):
        return self.build(self.rows)

class MinCombMatrix(Matrix):
    @classmethod
    def pairs(cls,sets,nr=None):
        if not nr:
            nr = len(sets)
        d = cls(nr)
        for set in sets:
            s = cls(nr)
            for i in xrange(nr):
                for j in xrange(nr):
                    if i in set and j in set:
                        s[i,j] = 1
            d = d + s
        return d

    # def sort_diagonal(self):

    def sorted_diagonal(self):
        m = self.__class__(self.nr,self.nc+1)
        m = m + self

        # add row index to last column
        for i,row in enumerate(m.rows):
            row[-1] = i

        # get array with the sorted positions of the diagonal
        sorted_diagonal = sorted(enumerate(self.diagonal()),key=lambda e: e[1])
        indexes = [e[0] for e in sorted_diagonal]

        # reorder by the indexes array
        sorted_m_rows = []
        for index in indexes:
             sorted_m_rows.append(m.rows[index])

        # return a new Matrix object with the sorted rows in place
        sorted_m = self.__class__.build(sorted_m_rows)
        return sorted_m

    def find_pair(self,r):
        sorted_m = self.sorted_diagonal()
        indexes = sorted_m.transpose().rows[-1]

        next_j = False

        for i in r[-1][::-1]:
            col = sorted_m.col(i)
            if 0 in col:
                next_j = indexes[col.index(0)]
                break

        return next_j

    def find_next(self):
        pass
        # obtener la fila con mayor numero de 0s de la matriz sorted_diagonal


if __name__ == "__main__":
    r = [[0,1,3],[1,4,0],[3,2]]
    m = MinCombMatrix.pairs(r,5)
    print m.find_pair(r)

