from numpy.random import randint
from operator import add, sub, neg, mul, floordiv
import traceback

class RollResult:
	def __init__(self, roll, detail):
		self._roll = roll
		self._detail = detail
		if detail:
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

def it(x, step):
	state = x
	while state > 0:
		if state > step:
			state -= step
			yield step
		else:
			yield state
			state = 0

class ThrowResult:
	_results = None

	def __init__(self, number, sides):
		self._number = number
		self._sides = sides
		self._detail = False

	def detail(self):
		self._detail = True
		self._sides.detail()
		self._number.detail()

	def define(self):
		sides = int(self._sides)+1
		number = int(self._number)
		if self._detail and int(self._sides) < 100:
			self._results = randint(1, sides, number)
		else:
			self._results = 0
			#self._results = sum(
					#map(lambda x: sum(randint(1, sides, x)),
						#it(number)))
			self._results = int(sum(map(lambda x: sum(randint(1, sides, x)), it(number, min(number, 10000000)))))

	def __repr__(self):
		if self._results is None:
			self.define()
		if self._detail != False:
			return '(' + '+'.join(map(str, self._results)) + ')'
		else:
			return str(self._results)

	def __int__(self):
		if self._results is None:
			self.define()
		if self._detail and int(self._sides) < 100:
			return int(sum(self._results))
		else:
			return int(self._results)

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
