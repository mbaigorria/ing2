class LandLot(object):

	def __init__(self, terrainType, distanceToReservoir):
		self.oilRig = None
		self.drillingRig = None
		self.terrainType = terrainType
		self.distanceToReservoir = distanceToReservoir
		self.drilledSoFar = 0

	def __str__(self):
		s = 'LandLot\n'
		s += 'oilRig: {}\n'.format(self.oilRig)
		s += 'drillingRig: {}\n'.format(self.drillingRig)
		s += 'terrainType: {}\n'.format(self.terrainType)
		s += 'distanceToReservoir: {}\n'.format(self.distanceToReservoir)
		s += 'drilledSoFar: {}\n'.format(self.drilledSoFar)
		return s

	def addDrillingRig(self, aDrillingRig):
		self.drillingRig = aDrillingRig

	def addOilRig(self, anOilRig):
		self.drillingRig = None
		self.oilRig = oilRig

	def drill(self, distance):
		self.drilledSoFar = min(self.drilledSoFar + distance, self.distanceToReservoir)

		drillingDone = self.drilledSoFar == self.distanceToReservoir
		return drillingDone


if __name__ == '__main__':

	aLandLot = LandLot()