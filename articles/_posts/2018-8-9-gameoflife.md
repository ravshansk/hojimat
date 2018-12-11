---
layout: post
title: Object-oriented Game of Life in Python
lang: english
categ: article
keywords: object-oriented, game of life, agent-based model
tags: economics complexity
redirect_from: /blog/2018/08/09/gameoflife/
image: /assets/img/gameoflife/time0.png
---

### Intro
I have been planning to build a superior GUI alternative to _NetLogo_ for a long time. When I finally started working on a project, I decided to test the basic implementations in Python. Sure enough, the first app was _Conway's Game of Life_ - a great special case of _cellular automata_.  

Can you imagine my surprise that I haven't found an object-oriented implementation of the game in Python --- all codes were either written in Java or in _imperative_ Python.  

So, I decided to build the model. I used two classes --- _Person_, which corresponded to each cell, and _Game_, which controlled the system dynamics. A great [article by _Giorgio Sironi_](https://dzone.com/articles/oo-vs-functional-game-life) also adviced to create a third class _Generation_, but I didn't find it necessary.  

### Model
So, first, I imported three libraries that I used:

```python
from math import ceil, floor, sqrt
import random
from matplotlib import pyplot as plt
```

Then I defined a _Person_ class with _(x,y)_-coordinates and empty vector of _alive-dead_ statuses for every time period. Every _Person_ object contains _neighbours_ method which returns adjacent cells and _kill-resurrect_ methods to change the life status:

```python
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
```

Then I defined a Game class with _setup_ method which randomly draws initial stage, and _stage_ method which executes system dynamics:

```python
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
```

So, this was it. Now, you just have to input number of rows and columns _(x,y)_ and number of time periods _t_ and play the game. The resulting plots will be exported to your working directory:

```python
# game:
a = Game(x,y,t)
a.play()
a.results()
# plot:
for j in range(t):
	b = []
	for i in range(x):
		b.append([z[2][j] for z in a.results() if z[0]==i])
	plt.spy(b)
	plt.savefig(f"time{j}.png")
```

For presentation purposes I animated the resulting graphs:

<figure class="blog">
	<img src="/assets/img/gameoflife/game.gif" alt="Game of life dynamics">
	<figcaption>"Game of life" dynamics</figcaption>
</figure>

### Conclusion
Here we go, I have built and shared the very basic object-oriented implementation of the very basic game in the most popular language, and somehow I ended up being the first one to do it. So, I will just leave it here as a starting point for future learners.  

Be sure to check my other posts in [_ravshansk.com/articles_](/articles) and to [_follow me on Twitter @ravshansk_](http://twitter.com/ravshansk).
