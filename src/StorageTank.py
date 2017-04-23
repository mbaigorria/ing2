class StorageTank(object):
	''' a storage tank can either store water or gas '''

	def __init__(self, constructionTime, constructionCost, storageCapacity):
		self.constructionTime = constructionTime
		self.constructionCost = constructionCost
		self.storageCapacity = storageCapacity

		# current storage parameters
		self.volumeStored = 0

	def __str__(self):
		s = 'Storage Tank\n'
		s += 'constructionTime: {}\n'.format(self.constructionTime)
		s += 'constructionCost: {}\n'.format(self.constructionCost)
		s += 'storageCapacity: {}\n'.format(self.storageCapacity)
		s += 'volumeStores: {}\n'.format(self.volumeStored)
		return s

	def store(self, volumeToStore):

		if volumeToStore > self.storageCapacity - self.volumeStored:
			print 'Error: storage exceeds the capacity of the tank.'
			exit()

		self.volumeStored += volumeToStore

	def extract(self, volumeToExtract):
		
		if volumeToExtract > self.volumeStored:
			print 'Error: current tank storage is not enough for extraction.'
			exit()

		self.volumeStored -= volumeToExtract

		return volumeToExtract


if __name__ == '__main__':

	aStorageTank = StorageTank()