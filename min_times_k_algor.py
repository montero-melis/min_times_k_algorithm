#!/usr/bin/env python

import itertools
import sys


class Results:
    def __init__(self,n,k):
        self.N = n
        self.K = k
        self.column  = []
        self.results = []

    def append(self, value):
        self.column.append(value)
        if self.column_complete():
            self.results.append(self.column)
            self.column = []

    def column_complete(self):
        return len(self.column) % self.K == 0

    def previous_values(self):
        return self.column[:]

    def pairs(self):
        r = self.results[:]
        r.append(self.column)

        existing_combinations = []

        for col in r:
            existing_combinations.extend(itertools.combinations(col,2))

        pairs = []
        # TODO: all combinations should already be stored
        for pair in itertools.combinations(range(self.N),2):
            count = len(filter(lambda x: x == pair, existing_combinations))
            pairs.append([pair,count])

        return pairs

class MinCombNK:
    """
    This is the class used to calculate the minimum number of ...
    Willy, a bit of literature here, s'il te plait !

    Instance variables:

        self.N

        self.K

        self.i:
            The current i-index.

        self.j:
            The current j-index.

        self.occurrences:
            A list that keeps record of the number of times an element has
            appeared.
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

        # O["occurr",]
        self.occurrences = [0] * self.N

        self.results = Results(self.N,self.K)

    def solve(self):
        self.results.append(self.i)
        self.occurrences[self.i] += 1

        contador = 0
        while not self.finished() and contador < 20:
            print "contador", contador
            contador += 1

            new_pair = False
            previous_values = self.results.previous_values()

            while not new_pair and len(previous_values) > 0:
                new_pair = self.find_pair()
                if not new_pair:
                    self.i = previous_values.pop()

            if new_pair:
                print "I got a new pair"
                # step 6
                self.j = new_pair

                # step 7
                self.results.append(self.j)
                self.occurrences[self.j] += 1
                self.recalculate_pairs(self.results.column)

                self.i = self.j
            else:
                print "no new pair"
                self.i = self.find_next()

                # step 2
                self.results.append(self.i)
                self.occurrences[self.i] += 1
                self.recalculate_pairs(self.results.column)
        print self.results.results

    def finished(self):
        # step 3, step 8
        if self.results.column_complete():
            if self.occurrences_complete():
                # step 4, step 9
                print self.results.results
                return True
        else:
            return False

    def find_pair(self):
        # que nos devuelva un j
        # o que falle y entonces tenemos que reasignar un i

        # buscamos un j que no haya sido emparejado con i
        # buscamos primero por los que hayan aparecido un minimo numero de veces

        for e in self.sorted_occurrences():
            if self.i == e:
                continue

            test_pair = tuple(sorted([self.i,e]))
            pair_occurrences = self.get_pair_occurrences(test_pair)

            if pair_occurrences == 0:
                return e

        return False

    def find_next(self):
        minimum_occurrences = min(self.occurrences_in_pairs())
        for n in [(e+self.i) % self.N for e in range(self.N)]:
            if self.occurrences_in_pairs()[n] == minimum_occurrences:
                return n

    def recalculate_pairs(self,column):
        pass

    def get_pair_occurrences(self,pair):
        return filter(lambda x: x[0] == pair, self.results.pairs())[0][1]

    def sorted_occurrences(self):
        occurrences = sorted(list(enumerate(self.occurrences)))
        sorted_list = sorted(occurrences, key=lambda x: x[1])

        return [e[0] for e in sorted_list]

    def occurrences_in_pairs(self):
        occurrences = []
        for i in range(self.N):
            count = 0
            for pair in self.results.pairs():
                if i in pair[0] and pair[1] > 0:
                    count += 1
            occurrences.append(count)
        return occurrences

    def occurrences_complete(self):
        return self.occurrences_in_pairs() == [self.N - 1] * self.N

    # IGNORE:
    # def next_i(self):
    #     """
    #     Increments the i-index by one, and wraps around the end of the list.
    #     """

    #     self.i = (self.i+1) % self.N
    #     return self.i

    # def find_i(self):
    #     """
    #     Returns the best guess for the next most optimum i-index.

    #     Algorithm: returns the first element after sorting them by occurrences
    #     as primary key, and occurrences_in_pairs as secondary key.
    #     """

    #     l = zip(range(self.N), self.occurrences, self.occurrences_in_pairs)
    #     sorted_l = sorted(l,key = lambda e: e[1:])
    #     return sorted_l[0][0]

    # def ordered_i(self):
    #     """
    #     Returns the element list rotated on the current i-index.
    #     """

    #     r = range(self.N)
    #     i = self.i
    #     return r[i:]+r[:i]

    # def append_result(self):
    #     pass

    # def complete(self):
    #     return False


min_t_k = MinCombNK(7,4)
min_t_k.solve()
