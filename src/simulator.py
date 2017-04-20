import random

class Log(object):

	def __init__(self):
		self.logRecords = []

	def addRecord(self, aRecord):
		print aRecord
		self.logRecords.append(aRecord)

	def export(filename):
		handle = open(filename, "w")
		handle.write('\n'.join(logRecords))
		handle.close()


class Simulator(object):

	def __init__(self, maxRigsInUse=10):
		self.maxRigsInUse = maxRigsInUse

	def createRandomExtractionArea(self, aReservoir):
		landLotList = [self.createRandomLandLot() for _ in range(random.randint(10, 100))]
		alpha_1 = random.uniform(0.1, 0.6)
		alpha_2 = random.uniform(0.01, 0.05)
		licitationTime = random.randint(10,100)
		return ExtractionArea(aReservoir, landLotList, licitationTime, alpha_1, alpha_2)

	def createRandomLandLot(self):
		terrainTypes = ['rocky', 'clay', 'normal']
		terrainType = terrainTypes[random.randint(0,len(terrainTypes)-1)]
		distanceToReservoir = random.random()
		return LandLot(terrainType, distanceToReservoir)

	def createRandomRigAvailabilityList(self):
		availableRigs = [self.createRandomRig() for _ in range(random.randint(10, 100))]
		return availableRigs

	def createRandomRig(self):
		dailyExcavationPower = random.random()
		rentPerDay = random.random()
		minRentPeriodInDays = random.randint(3,6)
		fuelConsumptionPerDay = random.random()
		return DrillingRig(dailyExcavationPower, rentPerDay, minRentPeriodInDays, fuelConsumptionPerDay)

	def getCurrentBeta(self):
		originalSize = self.extractionArea.reservoir.originalSize
		currentSize  = self.extractionArea.reservoir.currentSize
		enabledRigsCount = self.extractionArea.countEnabledOilRigs()
		return 	0.1*(currentSize/originalSize) / enabledRigsCount**(2/3)

	def updateBeta(self):
		self.extractionArea.betaSum += self.getCurrentBeta()

	def placeNewDrillingRigs(self, newDrillingRigs):
		''' newDrillingRigsPairs is a list of pairs (lot_id, drillingRig) '''
		for lot_id, newDrillingRig in newDrillingRigs:
			lot = self.extractionArea.landLots[lot_id]
			
			# test to see if there is something wrong
			if lot.drillingRig is not None or lot.oilRig is not None:
				print 'Error: a rig cannot be constructed in location {}'.format(lot_id)
				exit()

			lot.drillingRig = newDrillingRig

	def setEnabledRigs(self, enabledRigsList):
		for lot_id, lot in enumerate(self.extractionArea.landLots):
			if lot.oilRig is not None:
				if lot_id in enabledRigsList:
					lot.oilRig.isEnabled = True
				else:
					lot.oilRig.isEnabled = False

	def updateOilRigPressures(self):
		self.updateBeta()
		for lot in self.extractionArea.landLots:
			if lot.oilRig is not None:
				lot.oilRig.currentPressure *= self.getCurrentBeta()

	def getTotalExtraction():
		totalExtraction = 0
		for lot in self.extractionArea.landLots:
			if lot.oilRig is not None:
				totalExtraction += lot.oilRig.extractProduct(self.extractionArea)
		return totalExtraction

	def updateReservoirSize(self):
		totalExtraction = self.getTotalExtraction()
		self.extractionArea.reservoir.currentSize -= totalExtraction

	def startSimulation(self):

		# reservoir parameters (parametrize later?)
		sizeInCubicMeters = random.uniform(10**7,10**9)
		gasComposition = 0.2
		petrolComposition = 0.6

		reservoir = Reservoir(sizeInCubicMeters, gasComposition, petrolComposition)
		self.extractionArea = self.createRandomExtractionArea(reservoir)
		engineer = Engineer()
		
		# to ask: how often do we have new drilling rigs?
		availableRigs = self.createRandomRigAvailabilityList()

		currentTime = 0
		while engineer.decidesToKeepExtractingProduct(self.extractionArea, currentTime):
			newDrillingRigs = engineer.decidesNewDrillingRigs(extractionArea, availableRigs)
			pickedRigsToEnable = engineer.picksRigsToEnable(extractionArea, availableRigs, self.maxRigsInUse)
			self.placeNewDrillingRigs(newDrillingRigs)
			self.setEnabledRigs(pickedRigsToEnable)
			self.getTotalExtraction()
			self.updateReservoirSize()
			engineer.decidesReinjection()
			self.updateOilRigPressures()
			currentTime += 1


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


class Reservoir(object):

	def __init__(self, sizeInCubicMeters, gasComposition, petrolComposition):
		self.originalVolume = sizeInCubicMeters
		self.currentVolume = sizeInCubicMeters
		self.gasComposition = gasComposition
		self.petrolComposition = petrolComposition
		self.waterComposition = 1.0 - petrolComposition - gasComposition
		assert(self.waterComposition >= 0)

	def reinject(self, waterVolume, gasVolume):
			
		reinjectedVolume = waterVolume + gasVolume

		if reinjectedVolume + currentVolume > originalVolume:
			print 'Error: you cannot reinject more than the original volume.'
			exit()

		petrolComposition = petrolComposition*currentVolume/(currentVolume+reinjectedVolume)


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

	def addLandLot(self, aLandLot):
		self.landLots.append(aLandLot)

	def countEnabledOilRigs(self):
		enabledCount = 0
		for lot in self.landLots:
			if lot.oilRig is not None:
				enabledCount += lot.oilRig.isEnabled
		return enabledCount


class LandLot(object):

	def __init__(self, terrainType, distanceToReservoir):
		self.oilRig = None
		self.drillingRig = None
		self.terrainType = terrainType
		self.distanceToReservoir = distanceToReservoir
		self.drilledSoFar = 0

	def addDrillingRig(self, aDrillingRig):
		self.drillingRig = aDrillingRig

	def addOilRig(self, anOilRig):
		self.drillingRig = None
		self.oilRig = oilRig

	def drill(self, distance):
		self.drilledSoFar = min(self.drilledSoFar + distance, self.distanceToReservoir)

		drillingDone = self.drilledSoFar == self.distanceToReservoir
		return drillingDone


class DrillingRig(object):

	def __init__(self, dailyExcavationPower, rentPerDay, minRentPeriodInDays, fuelConsumptionPerDay):
		self.daysInUse = 0
		self.dailyExcavationPower = dailyExcavationPower
		self.rentPerDay = rentPerDay
		self.minRentPeriodInDays = minRentPeriodInDays
		self.fuelConsumptionPerDay = fuelConsumptionPerDay
		self.landLot = None

	def buildIn(self, aLandLot):
		self.landLot = aLandLot

	def drill(self):
		if self.landLot is None:
			print 'Error: drill needs to be built in a land lot before drilling.'

		maxDrilling = self.dailyExcavationPower * self.getLandTypeMultiplier(self.landLot.terrainType)

		self.landLot.drill(maxDrilling)

	def getLandTypeMultiplier(self, landType):
		return {'rocky': 0.4,
				'clay':  1.1,
				'normal': 1.0}.get(landType, 1.0)

class OilRig(object):

	def __init__(self, anExtractionArea, distanceToReservoir, initialPressure):
		self.isEnabled = False
		self.distanceToReservoir = distanceToReservoir
		self.currentPressure = self.calculatePressure(anExtractionArea, distanceToReservoir)
		self.initialPressure = initialPressure

	def calculatePressure(self, anExtractionArea, distanceToReservoir):
		initialPressure = calculateInitialPressure(distanceToReservoir)
		self.currentPressure = initialPressure * Math.exp(-anExtractionArea.betaSum)

	def calculateInitialPressure(distanceToReservoir):
		''' 
		it is not really specified, but the initial pressure of any rig could be different
		according to an email, the initial pressure is set on construction.
		'''
		return self.initialPressure

	def extractProduct(self, anExtractionArea):
		enabledRigs = anExtractionArea.countEnabledOilRigs()

		alpha_1 = anExtractionArea.alpha_1
		alpha_2 = anExtractionArea.alpha_2

		if not anOilRig.isEnabled:
			print 'Error: you cannot extract oil from an oil rig that is not enabled.'
			exit()

		extractedVolume = alpha_1*(self.currentPressure/enabledRigs) + alpha_2*(self.currentPressure/enabledRigs)**2

		return extractedVolume


class SeparatingPlant(object):

	def __init__(self, constructionTime, constructionCost, separatingCapacity):
		''' constructionTime is in days. separatingCapacity in cubic meters. '''
		self.constructionTime = constructionTime
		self.constructionCost = constructionCost
		self.separatingCapacity = separatingCapacity
		self.usedCapacity = 0

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

class StorageTank(object):

	def __init__(self, constructionTime, constructionCost, storageCapacity):
		self.constructionTime = constructionTime
		self.constructionCost = constructionCost
		self.storageCapacity = storageCapacity

		# current storage parameters
		self.waterStorage = 0
		self.gasStorage = 0
		self.usedCapacity = 0

	def store(self, gasVolume, waterVolume):

		if gasVolume + waterVolume > self.storageCapacity - self.usedCapacity:
			print 'Error: storage exceeds the capacity of the tank.'
			exit()

		self.waterStorage += waterVolume
		self.gasStorage += gasVolume
		self.usedCapacity += waterVolume + gasVolume

	def extractWater(self, extractionVolume):
		
		water, _ = self.extraction(extractionVolume, 0)
		return water

	def extractGas(self, extractionVolume):
		
		_, gas = self.extraction(0, extractionVolume)
		return gas

	def extraction(self, waterVolume, gasVolume):
		
		if gasVolume > self.gasStorage:
			print 'Error: current tank storage is not enough for extraction.'
			exit()

		if waterVolume > self.waterStorage:
			print 'Error: current tank storage is not enough for extraction.'
			exit()

		self.gasStorage -= gasVolume
		self.waterStorage -= waterVolume
		self.usedCapacity -+ gasVolume + waterVolume

		self.usedCapacity -= extractionVolume

		return waterVolume, gasVolume

if __name__ == '__main__':

	aSimulator = Simulator()
	aSimulator.startSimulation()