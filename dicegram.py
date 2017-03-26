import ply.lex as lex
import ply.yacc as yacc
from numpy.random import randint
from numpy import sum

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
		p[0] = p[1] - p[3]

	def p_subexpr_empty(self, p):
		'subexpr : addexpr'
		p[0] = p[1]

	def p_addexpr_rec(self, p):
		'addexpr : addexpr ADD divexpr'
		p[0] = p[1] + p[3]

	def p_addexpr_empty(self, p):
		'addexpr : divexpr'
		p[0] = p[1]

	def p_divexpr_rec(self, p):
		'divexpr : divexpr DIV mulexpr'
		p[0] = p[1] // p[3]

	def p_divexpr_empty(self, p):
		'divexpr : mulexpr'
		p[0] = p[1]

	def p_mulexpr_rec(self, p):
		'mulexpr : mulexpr MUL usubexpr'
		p[0] = p[1] * p[3]

	def p_mulexpr_empty(self, p):
		'mulexpr : usubexpr'
		p[0] = p[1]

	def p_usubexpr_neg(self, p):
		'usubexpr : SUB uambexpr'
		p[0] = - p[2]

	def p_usubexpr_empty(self, p):
		'usubexpr : throwexpr'
		p[0] = p[1]

	def p_throwexpr_throw(self, p):
		'throwexpr : uambexpr DICED uambexpr'
		p[0] = sum(randint(1, p[3]+1, p[1]))

	def p_throwexpr_empty(self, p):
		'throwexpr : uambexpr'
		p[0] = p[1]

	def p_uambexpr_num(self, p):
		'uambexpr : NUMBER'
		p[0] = p[1]

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
			return int(self.val)
		except ValueError:
			return None

if __name__ == "__main__":
	d = DiceGram()
	print(d.parse(input()))
