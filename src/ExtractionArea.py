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

		# containers for processing plants/storage
		self.separatingPlants = []
		self.storageTanks = []

	def __str__(self):
		s = 'ExtractionArea\n'
		s += 'Reservoir:\n {}'.format(self.reservoir)
		s += 'licitationTime: {}\n'.format(self.licitationTime)
		return s

	def addLandLot(self, aLandLot):
		self.landLots.append(aLandLot)

	def countEnabledOilRigs(self):
		enabledCount = 0
		for lot in self.landLots:
			if lot.oilRig is not None:
				enabledCount += lot.oilRig.isEnabled
		return enabledCount


if __name__ == '__main__':

	anExtractionArea = ExtractionArea()