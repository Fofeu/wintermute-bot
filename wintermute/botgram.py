import ply.lex as lex
import ply.yacc as yacc
import logging
from rollexpr import *
from parseresult import *
from parseexceptions import *
from mkmutils import *
import re

class BotGram(object):

	reserved_words = {
		'cdlamerde': 'CDLAMERDE',
		'roll': 'ROLL',
		'detail': 'DETAIL',
		'd': 'DICED',
		'D': 'DICED',
		'mtg': 'MTG',
		'store': 'STORE',
		'help': 'HELP'
	}

	tokens = (
		'MENTION',

		'ID',

		'CDLAMERDE',

		'ROLL',
		'DETAIL',
		'DECA',
		'HEXA',
		'OCTA',
		'BINA',
		'DICED',
		'ADD',
		'SUB',
		'MUL',
		'DIV',
		'LPAR',
		'RPAR',

		'MTG',

		'STORE',
		'LITERAL',

		'HELP'
	)

	precedence = (
		('left', 'DICED'),
		('left', 'ADD', 'SUB'),
		('left', 'MUL', 'DIV'),
		('right', 'NEG')
	)

	t_MENTION = r'<@[!0-9]*>'
	t_ADD = r'\+'
	t_SUB = r'-'
	t_MUL = r'\*'
	t_DIV = r'/'
	t_LPAR = r'\('
	t_RPAR = r'\)'
	t_ignore = r' '

	def t_DECA(self, t):
		r'[1-9][0-9]*'
		t.value = int(t.value)
		return t

	def t_HEXA(self, t):
		r'0x[0-9A-F]+'
		t.value = int(t.value, 16)
		return t

	def t_OCTA(self, t):
		r'0o[0-7]+'
		t.value = int(t.value, 8)
		return t

	def t_BINA(self, t):
		r'0b[01]+'
		t.value = int(t.value, 2)
		return t

	def t_ID(self, t):
		r'[a-zA-Z]+'
		t.type = self.reserved_words.get(t.value, 'ID')
		return t

	def t_LITERAL(self, t):
		r'"[^"]*"'
		t.value = t.value[1:-1]
		return t

	def t_error(self, t):
		raise LexerError(t)

	start = 'start'

	def p_start(self, p):
		'''start : MENTION rollcmd
		         | MENTION cdlamerdecmd
		         | MENTION mtgcmd
		         | MENTION storecmd
		         | MENTION helpcmd'''
		p[0] = p[2]
		p[0].mention = p[1]

	def p_cdlamerdecmd(self, p):
		'cdlamerdecmd : CDLAMERDE'
		p[0] = TextAnswer("Oui, maîîître !")

	def p_mtgcmd(self, p):
		'''mtgcmd : MTG'''
		p[0] = TextAnswer("MTG commands are not implemented yet")

	def p_storecmd(self, p):
		'storecmd : STORE string'
		p[0] = TextAnswer("Store commands are not implemented yet.")

	def p_helpcmd(self, p):
		'helpcmd : HELP opt_string'
		p[0] = TextAnswer(self.help_text(p[2]))

	# Strings

	def p_opt_string(self, p):
		'''opt_string : string
		              |'''
		if len(p) > 1:
			p[0] = p[1]
		else:
			p[0] = None

	def p_string_short(self, p):
		'string : ID'
		p[0] = p[1]

	def p_string_long(self, p):
		'string : LITERAL'
		p[0] = p[1]

	# Roll Language

	def p_rollcmd(self, p):
		'rollcmd : ROLL opt_detail rollexpr'
		p[0] = RollResult(p[3], p[2])

	def p_opt_detail_detail(self, p):
		'''opt_detail : DETAIL
		              |'''
		p[0] = len(p) > 1

	def p_rollexpr_sub(self, p):
		'rollexpr : rollexpr SUB rollexpr'
		p[0] = BinOpResult(sub, p[1], p[3])

	def p_rollexpr_add(self, p):
		'rollexpr : rollexpr ADD rollexpr'
		p[0] = BinOpResult(add, p[1], p[3])

	def p_rollexpr_div(self, p):
		'rollexpr : rollexpr DIV rollexpr'
		p[0] = BinOpResult(floordiv, p[1], p[3])

	def p_rollexpr_mul(self, p):
		'rollexpr : rollexpr MUL rollexpr'
		p[0] = BinOpResult(mul, p[1], p[3])

	def p_rollexpr_neg(self, p):
		'rollexpr : SUB rollexpr %prec NEG'
		p[0] = UnOpResult(neg, p[2])

	def p_rollexpr_throw(self, p):
		'rollexpr : rollexpr DICED rollexpr'
		p[0] = ThrowResult(p[1], p[3])

	def p_rollexpr_deca(self, p):
		'rollexpr : DECA'
		p[0] = ConstResult(p[1])

	def p_rollexpr_hexa(self, p):
		'rollexpr : HEXA'
		p[0] = ConstResult(p[1])

	def p_rollexpr_octa(self, p):
		'rollexpr : OCTA'
		p[0] = ConstResult(p[1])

	def p_rollexpr_bina(self, p):
		'rollexpr : BINA'
		p[0] = ConstResult(p[1])

	def p_rollexpr_par(self, p):
		'rollexpr : LPAR rollexpr RPAR'
		p[0] = p[2]

	def p_error(self, p):
		raise ParserError(p)

	# Non-language details
	prelude = None

	def __init__(self, prelude=None):
		self.prelude = prelude
		self.lexer = lex.lex(module=self)
		self.parser = yacc.yacc(module=self, write_tables=False)
		self.introspect()

	def introspect(self):
		self.parser_rules = list(filter(
			lambda x: re.match('^p_.*', x),
			self.__dir__()))
		self.parser_dir = {}
		for rule in self.parser_rules:
			if getattr(self,rule).__doc__ is not None:
				start, rules = self.extract_grammar(rule)
				if start not in self.parser_dir:
					self.parser_dir[start] = rules
				else:
					self.parser_dir[start] += rules

	def extract_grammar(self, rule):
		rule = self.__getattribute__(rule).__doc__
		rule_clean = re.sub('\%prec [A-Z]+', '',
			re.sub('  *', ' ', rule
			.replace('\n', ' ')
			.replace('\t', ' ')
			.replace(':', '|')))
		l = re.findall('[^\| ][^\|]*[^\| ]', rule_clean)
		start = l[0]
		rules = list(map(lambda x: x.split(' '),l[1:]))
		return start, rules

	def help_text(self, section):
		if section is None:
			return self.help_text(self.start)
		elif section in self.tokens:
			try:
				tok = getattr(self, 't_'+section)
			except AttributeError:
				tok = list(
					map(lambda kv: kv[0],
					filter(lambda kv: kv[1]==section,
					self.reserved_words.items())))
				tok = None if len(tok)==0 else tok
			desc = ' is a token'
			if type(tok) is str:
				desc += ' produced by rule `' + tok + '`'
			elif type(tok) is list:
				desc += ' produced by rules'
				for r in tok:
					desc += ' `' + r + '`'
			elif tok.__doc__ is not None:
				desc += ' produced by rule `' + tok.__doc__ + '`'
			return section + desc
		elif section not in self.parser_dir:
			return section + ' is not a known grammar rule'
		else:
			result = section + ':'
			try:
				result += getattr(self, 'help_' + section)
			except AttributeError:
				pass
			for rule in self.parser_dir[section]:
				result += '\n\t'
				result += ' '.join(rule)
			return '```'+result+'```'

	def parse_text(self, s):
		return self.parser.parse(s, lexer=self.lexer)

	def parse(self, mess):
		try:
			parsed = self.parse_text(mess.content)
			parsed.author = mess.author.mention
			parsed.prelude = self.prelude
			self.check(parsed, mess)
			return parsed
		except (LexerError,ParserError) as e:
			logging.info(e)
			pass
		except WronglyAddressedMessage:
			pass

	def check(self, parsed, mess):
		# Checks that the message is actually for us
		if parsed.mention != mess.channel.server.me.mention:
			raise WronglyAddressedMessage

if __name__ == "__main__":
	d = BotGram()
	r = d.parse_text("<@!132> " + input("Input: "))
	print(str(r))
