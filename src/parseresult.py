class TextAnswer:
	_text = None
	_mention = None
	def __init__(self, mention, text):
		self._text = text
		self._mention = mention

	def __str__(self):
		return str(self._text)
