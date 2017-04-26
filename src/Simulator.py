import random

from Reservoir import *
from LandLot import *
from ExtractionArea import *
from Engineer import *
from DrillingRig import *
from SeparatingPlant import *
from StorageTank import *

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
		self.bruteCost = 0
		self.bruteEarnings = 0

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

		def createRandomRig():
			dailyExcavationPower = random.random()*100
			rentPerDay = random.random()*100
			minRentPeriodInDays = random.randint(3,6)
			fuelConsumptionPerDay = random.random()*100
			return DrillingRig(dailyExcavationPower, rentPerDay, minRentPeriodInDays, fuelConsumptionPerDay)

		availableRigs = [createRandomRig() for _ in range(random.randint(10, 100))]
		return availableRigs

	def createRandom(self, elementType):
		''' uses constructor in elementType to create a random instance of the class '''
		constructionTime = random.randint(3,6)
		constructionCost = random.random()*100
		capacity = random.random()*100
		return elementType(constructionTime, constructionCost, capacity)

	def createRandomSeparatingPlantAvailabilityList(self):
		availablePlants = [self.createRandom(SeparatingPlant) for _ in range(random.randint(10,100))]
		return availablePlants

	def createRandomStorageTankAvailabilityList(self):
		availableTanks = [self.createRandom(StorageTank) for _ in range(random.randint(10,100))]
		return availableTanks

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

	def distributeExtractedProduct(self, totalExtraction):
		pass

	def distributeRefinedProduct(self):
		pass

	def extractGasFromTanks(self):
		pass

	def startSimulation(self):

		# reservoir parameters (parametrize later?)
		sizeInCubicMeters = random.uniform(10**7,10**9)
		gasComposition = 0.2
		petrolComposition = 0.6
		reinjectionLimit = random.random()*200

		gasPrice = random.random()
		oilPrice = random.random()

		reservoir = Reservoir(sizeInCubicMeters, gasComposition, petrolComposition, reinjectionLimit)
		self.extractionArea = self.createRandomExtractionArea(reservoir)
		engineer = Engineer()
		
		# to ask: how often do we have new drilling rigs?
		availableRigs = self.createRandomRigAvailabilityList()
		availableSeparatingPlants = self.createRandomSeparatingPlantAvailabilityList()
		availableTanks = self.createRandomStorageTankAvailabilityList()

		currentTime = 0
		while engineer.decidesToKeepExtractingProduct(self.extractionArea, currentTime):

			# calculate extraction of previous period
			totalExtraction = self.getTotalExtraction()

			# first we need to distribute the refined product, so it doesnt mix up with the extracted product
			self.distributeRefinedProduct()
			self.distributeExtractedProductBetweenRefinieries(totalExtraction)

			# once the extraction/reinjection occurs, update reservoir size and oil rig pressures.
			self.updateReservoirSize()
			self.updateOilRigPressures()

			# now the engineer starts to make decitions based on the current state of the extractionArea
			# drilling rigs
			newDrillingRigs = engineer.decidesNewDrillingRigs(extractionArea, availableRigs)
			pickedRigsToEnable = engineer.picksRigsToEnable(extractionArea, availableRigs, self.maxRigsInUse)
			cost = self.placeNewDrillingRigs(newDrillingRigs)
			self.bruteCost += cost
			self.setEnabledRigs(pickedRigsToEnable)

			# storage tanks
			newGasTanks, newWaterTanks = engineer.decidesNewStorageTanks(extractionArea, availableTanks)
			cost = self.placeNewTanks(newGasTanks, newWaterTanks)
			self.bruteCost += cost

			gasToSell, oilToSell = engineer.decidesToSell()
			self.extractGasFromTanks(gasToSell)
			self.bruteEarnings = gasToSell * gasPrice
			self.bruteEarnings = oilToSell * oilPrice

			waterVolumeToReinject, gasVolumeToReinject = engineer.decidesReinjection()
			reservoir.reinject(waterVolumeToReinject, gasVolumeToReinject)

			currentTime += 1

		print 'Total cost: {}'.format(self.bruteCost)
		print 'Total earnings: {}'.format(self.bruteEarnings)
		print 'Net earnings: {}'.format(self.bruteEarnings - self.bruteCost)	


if __name__ == '__main__':

	aSimulator = Simulator()
	aSimulator.startSimulation()