import re
from copy import deepcopy
import numpy as np

_regex = {"_mention" : re.compile("<@[!0-9]*> ")}

def strip_mentions(mess):
	return _regex["_mention"].sub('', mess)

def only_me(mess):
	return mess.mentions == [mess.server.me]

def limit_to(mess, target):
	return mess.channel == target[1]

def for_me(mess, regex=None):
	if regex:
		return only_me(mess) and _regex[regex].match(strip_mentions(mess.content))
	else:
		return only_me(mess)

def match(mess, regex):
	return _regex[regex].match(strip_mentions(mess.content)).groups()

def register_regex(name, regex):
	_regex[name] = re.compile(regex)
