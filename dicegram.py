import ply.lex as lex
import ply.yacc as yacc
from numpy.random import randint
from numpy import sum
from operator import add, sub, neg, mul, floordiv

class ExprResult():
	def __init__(self):
		pass

class ConstResult(ExprResult):
	def __init__(self, value):
		ExprResult.__init__(self)
		self._value = value

	def __repr__(self):
		return str(self._value)

	def __int__(self):
		return int(self._value)

class ThrowResult(ExprResult):
	def __init__(self, number, sides):
		self._number = number
		self._sides = sides
		self._results = randint(1, int(sides)+1, int(number))

	def __repr__(self):
		return '(' + '+'.join(map(str, self._results)) + ')'

	def __int__(self):
		return int(sum(self._results))

class BinOpResult(ExprResult):
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

class UnOpResult(ExprResult):
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

class DiceGram(object):
	tokens = (
		'NUMBER',
		'DICED',
		'ADD',
		'SUB',
		'MUL',
		'DIV',
		'LPAR',
		'RPAR'
	)

	t_DICED = r'[dD]'
	t_ADD = r'\+'
	t_SUB = r'-'
	t_MUL = r'\*'
	t_DIV = r'/'
	t_LPAR = r'\('
	t_RPAR = r'\)'
	t_ignore = r' '

	def t_NUMBER(self, t):
		r'\d+'
		t.value = int(t.value)
		return t

	def t_error(self, t):
		raise ValueError('Unable to parse string:\n' + t.value + '\n')

	start = 'start'
	
	def p_start(self, p):
		'start : expr'
		self.val = p[1]

	def p_expr(self, p):
		'expr : subexpr'
		p[0] = p[1]

	def p_subexpr_rec(self, p):
		'subexpr : subexpr SUB addexpr'
		p[0] = BinOpResult(sub, p[1], p[3])

	def p_subexpr_empty(self, p):
		'subexpr : addexpr'
		p[0] = p[1]

	def p_addexpr_rec(self, p):
		'addexpr : addexpr ADD divexpr'
		p[0] = BinOpResult(add, p[1], p[3])

	def p_addexpr_empty(self, p):
		'addexpr : divexpr'
		p[0] = p[1]

	def p_divexpr_rec(self, p):
		'divexpr : divexpr DIV mulexpr'
		p[0] = BinOpResult(floordiv, p[1], p[3])

	def p_divexpr_empty(self, p):
		'divexpr : mulexpr'
		p[0] = p[1]

	def p_mulexpr_rec(self, p):
		'mulexpr : mulexpr MUL usubexpr'
		p[0] = BinOpResult(mul, p[1], p[3])

	def p_mulexpr_empty(self, p):
		'mulexpr : usubexpr'
		p[0] = p[1]

	def p_usubexpr_neg(self, p):
		'usubexpr : SUB uambexpr'
		p[0] = UnOpResult(neg, p[2])

	def p_usubexpr_empty(self, p):
		'usubexpr : throwexpr'
		p[0] = p[1]

	def p_throwexpr_throw(self, p):
		'throwexpr : uambexpr DICED uambexpr'
		p[0] = ThrowResult(p[1], p[3])

	def p_throwexpr_empty(self, p):
		'throwexpr : uambexpr'
		p[0] = p[1]

	def p_uambexpr_num(self, p):
		'uambexpr : NUMBER'
		p[0] = ConstResult(p[1])

	def p_uambexpr_par(self, p):
		'uambexpr : LPAR expr RPAR'
		p[0] = p[2]

		
	def p_error(self, p):
		raise ValueError('Unable to parse string: ' + p.value)

	def __init__(self):
		self.lexer = lex.lex(module=self)
		self.parser = yacc.yacc(module=self)
		self.val = None

	def parse(self, s):
		try:
			self.parser.parse(s, lexer=self.lexer)
			return self.val
		except ValueError:
			return None

if __name__ == "__main__":
	d = DiceGram()
	r = d.parse(input())
	print(str(r), '=', int(r))
