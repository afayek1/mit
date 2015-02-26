#!/opt/local/bin python

import lib601.sm as sm

class Delay(sm.SM):
	def __init__(self, v0):
		self.startState = v0
 	
 	def getNextValues(self, state, inp):
		# Output is old state
		return (inp, state)


class Increment(sm.SM):
	startState = 0
	
	def __init__(self, incr):
		self.incr = incr
	
	def getNextValues(self, state, inp):
		return (state, inp + self.incr)



class Cascade(sm.SM):
	def __init__(self, sm1, sm2):
		self.m1 = sm1
		self.m2 = sm2
		self.startState = (sm1.startState, sm2.startState)

	
class Parallel(Cascade):
	"""
	Parallel machine with same input.
	"""
	def getNextValues(self, state, inp):
		(s1, s2) = state
		(newS1, o1) = self.m1.getNextValues(s1, inp)
		(newS2, o2) = self.m2.getNextValues(s2, inp)
		return ((newS1, newS2), (o1,o2))


class Parallel2(Cascade):
	"""
	Parallel machine with different inputs.
	"""
	def getNextValues(self, state, inp):
		(s1,s2) = state
		(i1,i2) = splitValue(inp)
		(newS1, o1) = self.m1.getNextValues(s1, i1)
		(newS2, o2) = self.m2.getNextValues(s2, i2)
		return ((newS1, newS2), (o1, o2))

def splitValue(v):
	"""
	Splits input. Actual deployment should check and generate errors for potential problems.
	"""
	if v == 'undefined':
		return ('undefined', 'undefined')
	else:
		return v


class PureFunction(sm.SM):
	def __init__(self, f):
		self.function = f
	
	def getNextValues(self, state, inp):
		return state, self.function(inp)



d = Delay(7)
d.transduce([3,1,2,5,9], verbose = True)
d100 = Delay(100)
d100.transduce([3,1,2,5,9], verbose = True)