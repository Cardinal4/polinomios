from functools import cmp_to_key

def lex(monomial_1: tuple, monomial_2: tuple):
    for i in range(len(monomial_1)):
        if monomial_1[i] > monomial_2[i]:
            return True
        elif monomial_1[i] < monomial_2[i]:
            return False

    return True

def grlex(monomial_1: tuple, monomial_2: tuple):
    sum_1 = sum(monomial_1)
    sum_2 = sum(monomial_2)

    if sum_1 == sum_2:
        return lex(monomial_1, monomial_2)
    else:
        return sum_1 > sum_2

class ZTuple:
    def __init__(self, z_tuple: tuple[int], order = grlex):
        for integer in z_tuple:
            if integer < 0:
                raise ValueError('Negative value in tuple')

        if type(z_tuple) != tuple:
            raise TypeError('ZTuple only accepts tuples')

        self.tuple = z_tuple
        self.order = order

    def __add__(self, z_tuple):
        if len(self.tuple) != len(z_tuple.tuple):
            raise IndexError('The tuples have not the same length')

        new_tuple = tuple([self.tuple[_] + z_tuple.tuple[_]
                           for _ in range(len(self.tuple))])

        return ZTuple(new_tuple)

    def __eq__(self, z_tuple):
        if type(self) != type(z_tuple):
            raise TypeError(type(z_tuple), 'is not comparable with ZTuple')

        return self.tuple == z_tuple.tuple

    def __hash__(self):
        return self.tuple.__hash__()

    def __gt__(self, z_tuple):
        if type(self) != type(z_tuple):
            raise TypeError(type(z_tuple), 'is not comparable with ZTuple')

        return self.order(self.tuple, z_tuple.tuple)

    def __iter__(self):
        return self.tuple.__iter__()

    def __len__(self):
        return len(self.tuple)
    
    def __getitem__(self, i):
        return self.tuple[i]

class Term:
    def __init__(self, coefficient, monomial_tuple: tuple,
                 variables: list[str], order = grlex):
        self.coefficient = coefficient
        self.monomial_tuple = ZTuple(z_tuple = monomial_tuple, order = order)
        self.variables = variables
        self.order = order

    def __eq__(self, term):
        if type(self) != type(term):
            raise TypeError(type(term), 'is not comparable with Term')

        return self.monomial_tuple == term.monomial_tuple\
            and self.coefficient == term.coefficient

    def __str__(self):
        if self.is_constant():
            return str(self.coefficient)
        string_representation = ''

        if self.coefficient != 1:            
            string_representation = str(self.coefficient)

        for i in range(len(self.monomial_tuple)):
            if(self.monomial_tuple[i] != 0):
                if(self.monomial_tuple[i] == 1):
                    string_representation += self.variables[i]
                else:
                    string_representation += self.variables[i]\
                        + '^' + str(self.monomial_tuple[i])
        
        return string_representation

    def __gt__(self, term):
        if type(self) != type(term):
            raise TypeError(type(term), 'is not comparable with Term')

        self.order(self.monomial_tuple, term.monomial_tuple)

    def __mul__(self, term):
        if type(self) != type(term):
            raise TypeError(type(term), 'is not comparable with Term')

        new_coeff = self.coefficient * term.coefficient
        new_tuple = self.monomial_tuple + term.monomial_tuple

        return Term(new_coeff, new_tuple.tuple, self.variables, self.order)

    def is_constant(self):
        zero_tuple = ZTuple(tuple([0] * len(self.monomial_tuple)),
                            order = self.order)

        return zero_tuple == self.monomial_tuple

class Polynomial:
    def __init__(self, terms: list[Term], variables: list[str], order = grlex):
        self.terms = terms
        self.variables = variables
        self.order = order
        self.clean()

    def clean(self):
        monomials = set([term.monomial_tuple for term in self.terms])
        new_terms = []

        for monomial in monomials:
            sum_coef = 0

            for term in self.terms:
                if term.monomial_tuple == monomial:
                    sum_coef += term.coefficient

            if sum_coef != 0:
                new_terms.append(Term(sum_coef, monomial.tuple, self.variables))

        self.terms = new_terms
        self.sort()

    def __str__(self):
        string_representation = ''

        for term in self.terms:
            string_representation += str(term) + ' + '

        return string_representation[0 : -2]

    def __add__(self, poly):
        if type(self) != type(poly):
            raise TypeError(type(poly), 'is not comparable with Poynomial')

        h = Polynomial(self.terms + poly.terms, self.variables, self.order)
        h.clean()

        return h

    def __mul__(self, poly):
        if type(self) != type(poly):
            raise TypeError(type(poly), 'is not comparable with Polynomial')

        h = Polynomial([term1 * term2 for term1 in self.terms
                        for term2 in poly.terms], self.variables, self.order)
        h.clean()

        return h

    @staticmethod
    def compare(order):
        def inner(term_1, term_2):
            monomial_1 = term_1.monomial_tuple
            monomial_2 = term_2.monomial_tuple

            if monomial_1 == monomial_2:
                return 0
            elif order(monomial_1, monomial_2):
                return -1
            else:
                return 1
            
        return inner

    def sort(self):
        self.terms = sorted(self.terms,
                            key = cmp_to_key(Polynomial.compare(self.order)))

'''vars = ['x', 'y']

t1 = Term(2, (1, 3), vars)
t2 = Term(3, (0, 3), vars)
t3 = Term(1, (0, 1), vars)
t4 = Term(1, (1, 0), vars)

f = Polynomial([t1, t2, t3, t4], vars, order = grlex)
g = Polynomial([t1, t2, t3, t4], vars, order = grlex)

print(f)
print(g)
print(f + g)

t1 = Term(2, (1, 1), ['x', 'y'])
t2 = Term(3, (1, 0), ['x', 'y'])
print(t1 * t2)'''

t1 = Term(1, (0,), ['x'])
t2 = Term(1, (1,), ['x'])
t3 = Term(-1, (0,), ['x'])
t4 = Term(1, (1,), ['x'])

f = Polynomial([t1, t2], ['x'])
g = Polynomial([t3, t4, t3], ['x'])
print(f * g)