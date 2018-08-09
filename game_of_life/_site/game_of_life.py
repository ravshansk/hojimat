import random
from matplotlib import pyplot as plt

class Person:
	people = []

	def __init__(self,x,y,alive):
		self.x = x
		self.y = y
		self.alive = alive
		Person.people.append(self)
		return
	
	def kill(self,t):
		self.alive[t] = False
		return
	
	def resurrect(self,t):
		self.alive[t] = True
		return

	def neighbours(self):
		a = []
		people = Person.people
		a += [z for z in people if z.x == self.x and z.y == self.y+1]
		a += [z for z in people if z.x == self.x and z.y == self.y-1]
		a += [z for z in people if z.x == self.x-1 and z.y == self.y]
		a += [z for z in people if z.x == self.x-1 and z.y == self.y+1]
		a += [z for z in people if z.x == self.x-1 and z.y == self.y-1]
		a += [z for z in people if z.x == self.x+1 and z.y == self.y-1]
		a += [z for z in people if z.x == self.x+1 and z.y == self.y+1]
		a += [z for z in people if z.x == self.x+1 and z.y == self.y]
		return a

	def alive_neighbours(self,t):
		a = [z for z in self.neighbours() if z.alive[t]]
		return a

class Game:
	def __init__(self, n, m, t):
		self.n = n
		self.m = m
		self.t = t
		return
	
	def setup(self):
		for i in range(self.n):
			for j in range(self.m):
				a = [False]*self.t
				a[0] = random.choice([True, False])
				Person(i,j,a)
		return

	def stage(self, t):
		for person in Person.people:
			if person.alive[t-1]:
				if len(person.alive_neighbours(t-1))<2:
					person.kill(t)
				if len(person.alive_neighbours(t-1)) in [2,3]:
					person.resurrect(t)
				if len(person.alive_neighbours(t-1))>3:
					person.kill(t)
			else:
				if len(person.alive_neighbours(t-1))==3:
					person.resurrect(t)
		return

	def play(self):
		self.setup()
		for i in range(1,self.t):
			self.stage(i)
		return

	def results(self):
		people = Person.people
		a = [[z.x, z.y, z.alive] for z in people]
		print(a)
		return a

#################################

a = Game(5,5,3)
a.play()
a.results()

# plot
b = [[2,2]]
plt.spy(b)
plt.show()
