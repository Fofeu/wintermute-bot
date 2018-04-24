class ParseResult:
	mention = None
	author = None
	prelude = None

	def __str__(self):
		raise NotImplementedError

class TextAnswer(ParseResult):
	text = None
	def __init__(self, text):
		self.text = text

	def __str__(self):
		result = [self.prelude, self.author, self.text]
		return " ".join(map(str, result))
