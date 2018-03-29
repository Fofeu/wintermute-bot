def unbignum(x, step):
	state = x
	while state > 0:
		if state > step:
			state -= step
			yield step
		else:
			yield state
			state = 0

def composemess(x):
	return (x[0], x[1] + str(x[2]))
