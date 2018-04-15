import ply.lex as lex
import ply.yacc as yacc
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
		p[0] = TextAnswer(p[1], p[2])

	def p_cdlamerdecmd(self, p):
		'cdlamerdecmd : CDLAMERDE'
		p[0] = "Oui, maîîître !"

	def p_mtgcmd(self, p):
		'''mtgcmd : MTG'''
		p[0] = "MTG commands are not implemented yet"

	def p_storecmd(self, p):
		'storecmd : STORE string'
		p[0] = "Store commands are not implemented yet. However, I would have stored " + p[3]

	def p_helpcmd(self, p):
		'helpcmd : HELP string'
		p[0] = self.help_text(p[2])

	# Strings

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

	def p_uambexpr_deca(self, p):
		'uambexpr : DECA'
		p[0] = ConstResult(p[1])

	def p_uambexpr_hexa(self, p):
		'uambexpr : HEXA'
		p[0] = ConstResult(p[1])

	def p_uambexpr_octa(self, p):
		'uambexpr : OCTA'
		p[0] = ConstResult(p[1])

	def p_uambexpr_bina(self, p):
		'uambexpr : BINA'
		p[0] = ConstResult(p[1])

	def p_uambexpr_par(self, p):
		'uambexpr : LPAR rollexpr RPAR'
		p[0] = p[2]


	def p_error(self, p):
		raise ParserError(p)

	def __init__(self):
		self.lexer = lex.lex(module=self)
		self.parser = yacc.yacc(module=self, write_tables=False)
		self.introspect()

	def introspect(self):
		self.parser_rules = list(filter(
			lambda x: re.match('^p_.*', x),
			self.__dir__()))
		self.parser_dir = {}
		for rule in self.parser_rules:
			if self.__getattribute__(rule).__doc__ is not None:
				start, rules = self.extract_grammar(rule)
				if start not in self.parser_dir:
					self.parser_dir[start] = rules
				else:
					self.parser_dir[start] += rules

	def extract_grammar(self, rule):
		rule = self.__getattribute__(rule).__doc__
		rule_clean = re.sub('  *', ' ', rule
			.replace('\n', ' ')
			.replace('\t', ' ')
			.replace(':', '|'))
		l = re.findall('[^\| ][^\|]*[^\| ]', rule_clean)
		start = l[0]
		rules = list(map(lambda x: x.split(' '),l[1:]))
		return start, rules

	def help_text(self, section):
		if section is None:
			return self.help_text(self.start)
		elif section in self.tokens:
			return section + ' is a token'
		elif section not in self.parser_dir:
			return section + ' is not a known grammar rule'
		else:
			result = section + ':'
			for rule in self.parser_dir[section]:
				result += '\n\t'
				result += ' '.join(rule)
			return result

	def parse_text(self, s):
		return self.parser.parse(s, lexer=self.lexer)

	def parse(self, mess):
		try:
			parsed = self.parser.parse(mess.content, lexer=self.lexer)
			self.check(parsed, mess)
			return parsed
		except (LexerError,ParserError) as e:
			print(e)
			pass
		except WronglyAddressedMessage:
			pass

	def check(self, parsed, mess):
		# Checks that the message is actually for us
		if parsed._mention != mess.channel.server.me.mention:
			raise WronglyAddressedMessage

if __name__ == "__main__":
	d = BotGram()
	r = d.parse_text("<@!132> " + input("Input: "))
	print(str(r))
