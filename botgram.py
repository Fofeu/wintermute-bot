import ply.lex as lex
import ply.yacc as yacc
from exprresult import *
from parseresult import *
from parseexceptions import *

class BotGram(object):
	tokens = (
		'MENTION',
		'CDLAMERDE',
		'ROLL',
		'DETAIL',
		'NUMBER',
		'DICED',
		'ADD',
		'SUB',
		'MUL',
		'DIV',
		'LPAR',
		'RPAR'
	)

	t_MENTION = r'<@[!0-9]*>'
	t_CDLAMERDE = r'cdlamerde!'
	t_ROLL = r'roll'
	t_DETAIL = r'detail'
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
		raise ValueError('Unable to tokenize string:\n' + t.value + '\n')

	start = 'start'
	
	def p_start(self, p):
		'''start : MENTION rollcmd
		         | MENTION cdlamerdecmd'''
		print(self.mess.channel.server.me.mention)
		print(p[1])
		if self.mess.channel.server.me.mention != p[1]:
			raise WronglyAddressedMessage()
		self.val = p[2]

	def p_cdlamerdecmd(self, p):
		'cdlamerdecmd : CDLAMERDE'
		p[0] = TextAnswer("Oui, maîîître !")

	def p_rollcmd_simple(self, p):
		'rollcmd : ROLL rollexpr'
		p[0] = RollResult(p[2], False)

	def p_rollcmd_detail(self, p):
		'rollcmd : ROLL DETAIL rollexpr'
		p[0] = RollResult(p[3], True)

	def p_rollexpr_init(self, p):
		'rollexpr : subexpr'
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
		'uambexpr : LPAR rollexpr RPAR'
		p[0] = p[2]

		
	def p_error(self, p):
		raise ValueError('Unable to parse string: ' + p.value)

	def __init__(self, discord):
		self.lexer = lex.lex(module=self)
		self.parser = yacc.yacc(module=self)
		self.val = None
		self._discord = discord

	def parse(self, s):
		try:
			self.parser.parse(s, lexer=self.lexer)
			return self.val
		except ValueError as e:
			#return TextAnswer(e[0])
			print('c')
			pass
		except WronglyAddressedMessage:
			print('d')
			pass

	def parse_mess(self, mess):
		self.mess = mess
		return self.parse(mess.content)

if __name__ == "__main__":
	d = BotGram(None)
	r = d.parse(input())
	print(str(r), '=', int(r))
