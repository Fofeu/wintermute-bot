from numpy.random import randint
from numpy import sum
from operator import add, sub, neg, mul, floordiv
from itertools import repeat

class RollResult:
	def __init__(self, roll, detail):
		self._roll = roll
		self._detail = detail
		self._roll.detail()

	def __repr__(self):
		if self._detail:
			return str(self._roll) + ' = ' + str(int(self._roll))
		else:
			return str(int(self._roll))

class ConstResult:
	def __init__(self, value):
		self._value = value

	def detail(self):
		pass

	def __repr__(self):
		return str(self._value)

	def __int__(self):
		return int(self._value)

class ThrowResult:
	def __init__(self, number, sides):
		self._number = number
		self._sides = sides
		self._results = None
		self._detail = False

	def detail(self):
		self._detail = True

	def define(self):
		if self._detail:
			self._results = randint(1, int(self._sides)+1, int(self._number))
		else:
			self._results = sum(map(lambda x: randint(1, int(self._sides)+1, 1), repeat(None, int(self._number))))

	def __repr__(self):
		if self._results is None:
			self.define()
		if self._detail != False:
			return '(' + '+'.join(map(str, self._results)) + ')'
		else:
			return self._results

	def __int__(self):
		if self._results is None:
			self.define()
		if self._detail:
			return int(sum(self._results))
		else:
			return self._results

class BinOpResult:
	def __init__(self, op, l, r):
		self._op = op
		self._l = l
		self._r = r

	def detail(self):
		self._l.detail()
		self._r.detail()

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

	def detail(self):
		self._v.detail()

	def _opstr(self):
		if self._op is neg:
			return '-'

	def __repr__(self):
		return self._opstr() + '(' + str(self._v) + ')'

	def __int__(self):
		return self._op(int(self._v))
