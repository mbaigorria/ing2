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

		volumeToSeparate = min(volumeToSeparate, self.separatingCapacity - self.usedCapacity)

		# update volume composition in separating plant
		self.gasComposition = self.gasComposition * self.usedCapacity + gasComposition / (self.usedCapacity + volumeToSeparate)
		self.petrolComposition = self.petrolComposition * self.usedCapacity + petrolComposition / (self.usedCapacity + volumeToSeparate)
		self.waterComposition = 1.0 - petrolComposition - gasComposition

		self.usedCapacity += volumeToSeparate

		return volumeToSeparate		

	def separateProducts(self, volumeToSeparate):

		volumeToSeparate = min(volumeToSeparate, self.usedCapacity)

		gas    = self.volumeToSeparate * self.gasComposition
		petrol = self.volumeToSeparate * self.petrolComposition
		water  = self.volumeToSeparate * self.waterComposition

		self.usedCapacity -= volumeToSeparate

		return gas, petrol, water


if __name__ == '__main__':

	aSeparatingPlant = SeparatingPlant()