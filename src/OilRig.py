class OilRig(object):

	def __init__(self, anExtractionArea, distanceToReservoir, initialPressure):
		self.isEnabled = False
		self.distanceToReservoir = distanceToReservoir
		self.currentPressure = self.calculatePressure(anExtractionArea, distanceToReservoir)
		self.initialPressure = initialPressure
		self.extractionArea = anExtractionArea

	def __str__(self):
		s = 'Oil Rig\n'
		s += 'isEnabled: {}\n'.format(self.isEnabled)
		s += 'distanceToReservoir: {}\n'.format(self.distanceToReservoir)
		s += 'currentPressure: {}\n'.format(self.currentPressure)
		s += 'initialPressure: {}\n'.format(self.initialPressure)
		return s

	def calculatePressure(self, anExtractionArea, distanceToReservoir):
		initialPressure = calculateInitialPressure(distanceToReservoir)
		self.currentPressure = initialPressure * Math.exp(-anExtractionArea.betaSum)

	def calculateInitialPressure(self, distanceToReservoir):
		''' 
		it is not really specified, but the initial pressure of any rig could be different
		according to an email, the initial pressure is set on construction.
		'''
		return self.initialPressure

	def extractProduct(self):
		enabledRigs = anExtractionArea.countEnabledOilRigs()

		alpha_1 = self.extractionArea.alpha_1
		alpha_2 = self.extractionArea.alpha_2

		if not anOilRig.isEnabled:
			print 'Error: you cannot extract oil from an oil rig that is not enabled by the Engineer.'
			exit()

		maxExtractionVolume = alpha_1*(self.currentPressure/enabledRigs) + alpha_2*(self.currentPressure/enabledRigs)**2

		return extractionArea.reservoir.extract(maxExtractionVolume)


if __name__ == '__main__':

	anOilRig = OilRig()