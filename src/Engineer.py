class Engineer(object):

	def decidesNewDrillingRigs(self, anExtractionArea, listOfAvailableRigs):
		pass

	def picksRigsToEnable(self, anExtractionArea, maxRigsInUse):
		pass

	def calculatesPotentialDailyVolume(self, anExtractionArea, anOilRig):
		initialPressure = anOilRig.initialPressure
		enabledRigs = anExtractionArea.countEnabledOilRigs()

		alpha_1 = anExtractionArea.alpha_1
		alpha_2 = anExtractionArea.alpha_2

		if anOilRig.isEnabled:
			enabledRigs += 1

		oilRigPressure = anOilRig.currentPressure
		potentialVolume = alpha_1*(oilRigPressure/enabledRigs) + alpha_2*(oilRigPressure/enabledRigs)**2

		return potentialVolume

	def decidesReinjection():
		''' if oil is reinjected, remember oil rig pressures must then be updated '''
		pass

	def decidesToKeepExtractingProduct(self, anExtractionArea, currentTime):
		if not self.decidesAreaIsStillProfitable(anExtractionArea):
			return False
		if currentTime >= anExtractionArea.licitationTime:
			return False

		# TODO: critic dilution, max expenditure.
		pass

	def decidesAreaIsStillProfitable(self, anExtractionArea):
		return True

	def decidesToSellGas(self):
		# check how much gas is available in the storage tanks, and sell it all or keep some for reinjection.
		pass

if __name__ == '__main__':

	anEngineer = Engineer()