from numpy.random import randint
from numpy import sum
from operator import add, sub, neg, mul, floordiv

class RollResult:
	def __init__(self, roll, detail):
		self._roll = roll
		self._detail = detail

	def __repr__(self):
		if self._detail:
			return str(self._roll) + ' = ' + str(int(self._roll))
		else:
			return str(int(self._roll))

class ConstResult:
	def __init__(self, value):
		self._value = value

	def __repr__(self):
		return str(self._value)

	def __int__(self):
		return int(self._value)

class ThrowResult:
	def __init__(self, number, sides):
		self._number = number
		self._sides = sides
		self._results = randint(1, int(sides)+1, int(number))

	def __repr__(self):
		return '(' + '+'.join(map(str, self._results)) + ')'

	def __int__(self):
		return int(sum(self._results))

class BinOpResult:
	def __init__(self, op, l, r):
		self._op = op
		self._l = l
		self._r = r

	def _opstr(self):
		if self._op is add:
			return '+'
		elif self._op is sub:
			return '-'
		elif self._op is mul:
			return '*'
		elif self._op is floordiv:
			return '/'

	def __repr__(self):
		return '(' + str(self._l) + ')' + self._opstr() + '(' + str(self._r) + ')'

	def __int__(self):
		return self._op(int(self._l), int(self._r))

class UnOpResult:
	def __init__(self, op, v):
		self._op = op
		self._v = v

	def _opstr(self):
		if self._op is neg:
			return '-'

	def __repr__(self):
		return self._opstr() + '(' + str(self._v) + ')'

	def __int__(self):
		return self._op(int(self._v))
