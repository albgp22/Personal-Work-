#Genetic Algorithm for Sudokus

import numpy as np
import random
import sys

class Sudoku:
	def __init__(self):
		self.modified=True
		self.last_opt=0
		self.grid=[]
		for i in range(9):
			curr=[]
			for j in range(9):
				curr.append(random.randint(1,9))
			self.grid.append(curr)
		self.grid=np.array(self.grid)

	@staticmethod
	def loss_row_col(arr):
		return sum([np.abs(1-i) for i in np.bincount(arr)])

	def mutate(self):
		self.modified=True
		for numb in range(random.randint(1,10)):
			i,j=random.randint(0,8), random.randint(0,8)
			self.grid[i][j]=random.randint(1,9)

	def mix(self, other):
		for i in range(3):
			for j in range(3):

				val1=Sudoku.loss_row_col(self.grid[i*3:i*3+3,j*3:j*3+3].flatten())
				val2=Sudoku.loss_row_col(other.grid[i*3:i*3+3,j*3:j*3+3].flatten())
				if val2<val1:
					self.grid[i*3:i*3+3,j*3:j*3+3]=other.grid[i*3:i*3+3,j*3:j*3+3]

		for i in range(9):

			val1=Sudoku.loss_row_col(self.grid[i,:])
			val2=Sudoku.loss_row_col(other.grid[i,:])
			if val2<val1:
				self.grid[i,:]=other.grid[i,:]

			val1=Sudoku.loss_row_col(self.grid[:,i])
			val2=Sudoku.loss_row_col(other.grid[:,i])
			if val2<val1:
				self.grid[:,i]=other.grid[:,i]




	def optimality_function(self):
		if not self.modified:
			return self.last_opt

		ret=0
		for i in range(9):
			ret+=Sudoku.loss_row_col(self.grid[i,:])+Sudoku.loss_row_col(self.grid[:,i])
		for i in range(3):
			for j in range(3):
				ret+=Sudoku.loss_row_col(self.grid[i*3:i*3+3,j*3:j*3+3].flatten())
		self.last_opt=ret
		self.modified=False
		return ret

class Population:
	def __init__(self, n_individuals):
		self.population=[]
		for i in range(n_individuals):
			self.population.append(Sudoku())

	def evolve(self):
		self.population=sorted(self.population, key=lambda i: i.optimality_function())

		if random.random()<.5:
			self.population.remove(self.population[len(self.population)-1])
			self.population.append(Sudoku())

		for i in self.population[1:]:
			if random.random()<.03:
				i.mutate()

		length=len(self.population)
		for i in range(length):
			for j in range(length):
				if not i==j:
					if random.random()<(length-i)*(length-j)/length**2:
						self.population[i].mix(self.population[j])

	def get_scores(self):
		return [x.optimality_function() for x in  sorted(self.population, key=lambda i: i.optimality_function())]

	def get_population(self):
		return sorted(self.population, key=lambda i: i.optimality_function())

P=Population(50)
for i in range(100000):
	P.evolve()
	if i%10==0:
		print(i)
	if i%100==0:
		sc=P.get_scores()
		print(sc)
		if 0 in sc:
			print("Sudoku Resuelto!!!")
			print (P.get_population()[0])
			sys.exit(0)





