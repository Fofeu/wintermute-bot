def unbignum(x, step):
	state = x
	while state > 0:
		if state > step:
			state -= step
			yield step
		else:
			yield state
			state = 0
