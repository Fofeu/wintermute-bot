class WronglyAddressedMessage(Exception):
	pass

class LexerError(Exception):
	value = None
	def __init__(self, name):
		self.value = name

class ParserError(Exception):
	value = None
	def __init__(self, name):
		self.value = name

