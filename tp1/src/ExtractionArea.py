class ExtractionArea(object):

	def __init__(self, aReservoir, aLandLotList, licitationTime, alpha_1, alpha_2):
		self.reservoir = aReservoir
		self.landLots = aLandLotList
		self.licitationTime = licitationTime

		# parameters to calculate potential volume of oil rigs.
		self.alpha_1 = alpha_1
		self.alpha_2 = alpha_2

		# beta will acummulate the sum of beta_i for i <= T.
		self.betaSum = 0

		# container for processing plants
		self.separatingPlants = []

		# containers for storage tanks
		self.gasTanks = []
		self.waterTanks = []

	def __str__(self):
		s = 'ExtractionArea\n'
		s += 'Reservoir:\n {}'.format(self.reservoir)
		s += 'licitationTime: {}\n'.format(self.licitationTime)
		return s

	def addLandLot(self, aLandLot):
		self.landLots.append(aLandLot)

	def addSeparatingPlant(self, aSeparatingPlant):
		self.separatingPlants.append(aSeparatingPlant)

	def addGasTank(self, aStorageTank):
		self.gasTanks.append(aStorageTank)

	def addWaterTank(self, aStorageTank):
		self.waterTanks.append(aStorageTank)

	def enabledOilRigsCount(self):
		enabledCount = 0
		for lot in self.landLots:
			if lot.oilRig is not None:
				enabledCount += lot.oilRig.isEnabled
		return enabledCount

	def storageStatus(self):
		waterStored = 0
		waterCapacity = 0

		gasStored = 0
		gasCapacity = 0

		for t in waterTanks:
			waterStored += t.volumeStored
			waterCapacity += t.storageCapacity
			
		for t in gasTanks:
			gasStored += t.volumeStored
			gasCapacity += t.storageCapacity

		return waterStored, waterCapacity, gasStored, gasCapacity

if __name__ == '__main__':

	anExtractionArea = ExtractionArea()