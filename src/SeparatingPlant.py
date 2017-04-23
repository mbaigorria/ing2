class SeparatingPlant(object):

	def __init__(self, constructionTime, constructionCost, separatingCapacity):
		''' constructionTime is in days. separatingCapacity in cubic meters. '''
		self.constructionTime = constructionTime
		self.constructionCost = constructionCost
		self.separatingCapacity = separatingCapacity
		self.usedCapacity = 0

	def __str__(self):
		s = 'Separating Plant\n'
		s += 'constructionTime: {}\n'.format(self.constructionTime)
		s += 'constructionCost: {}\n'.format(self.constructionCost)
		s += 'separatingCapacity: {}\n'.format(self.separatingCapacity)
		s += 'usedCapacity: {}\n'.format(self.usedCapacity)
		return s

	def receiveVolume(self, volumeToSeparate, gasComposition, petrolComposition):
		''' in every period, the plant separates all the volume it contains. therefore
		there wont be different concentration mixtures since the reservoir composition
		is the same for all rigs '''

		if volumeToSeparate > self.separatingCapacity:
			print 'Error: a separating plant cannot separate more than it\'s capacity.'
			exit()

		self.gasComposition = gasComposition
		self.petrolComposition = petrolComposition
		self.waterComposition = 1.0 - petrolComposition - gasComposition

		self.usedCapacity += volumeToSeparate

	def separateProducts(self):

		gas    = self.usedCapacity * self.gasComposition
		petrol = self.usedCapacity * self.petrolComposition
		water  = self.usedCapacity * self.waterComposition

		self.usedCapacity = 0

		return gas, petrol, water


if __name__ == '__main__':

	aSeparatingPlant = SeparatingPlant()