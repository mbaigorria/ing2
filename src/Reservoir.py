class Reservoir(object):

	def __init__(self, sizeInCubicMeters, gasComposition, petrolComposition, reinjectionLimit):
		self.originalVolume = sizeInCubicMeters
		self.currentVolume = sizeInCubicMeters
		self.gasComposition = gasComposition
		self.petrolComposition = petrolComposition
		self.waterComposition = 1.0 - petrolComposition - gasComposition
		self.reinjectionLimit = reinjectionLimit
		assert(self.waterComposition >= 0)

	def reinject(self, waterVolume, gasVolume):
			
		reinjectedVolume = waterVolume + gasVolume

		if reinjectedVolume + currentVolume > originalVolume:
			print 'Error: you cannot reinject more than the original volume.'
			exit()

		if reinjectedVolume > reinjectionLimit:
			print 'Error: you are exceeding the reinjection limit of the reservoir.'
			exit()

		self.petrolComposition = (self.petrolComposition*self.currentVolume)/(self.currentVolume+self.reinjectedVolume)
		self.gasComposition = (self.gasComposition*self.currentVolume+self.gasComposition)/(self.currentVolume+self.reinjectedVolume)
		self.waterComposition = 1 - self.petrolComposition - gasComposition


if __name__ == '__main__':

	aReservoir = Reservoir()