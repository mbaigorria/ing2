class DrillingRig(object):

	def __init__(self, dailyExcavationPower, rentPerDay, minRentPeriodInDays, fuelConsumptionPerDay):
		self.daysInUse = 0
		self.dailyExcavationPower = dailyExcavationPower
		self.rentPerDay = rentPerDay
		self.minRentPeriodInDays = minRentPeriodInDays
		self.fuelConsumptionPerDay = fuelConsumptionPerDay
		self.landLot = None

	def __str__(self):
		s = 'Drilling Rig\n'
		s += 'daysInUse: {}\n'.format(self.daysInUse)
		s += 'dailyExcavationPower: {}\n'.format(self.dailyExcavationPower)
		s += 'rentPerDay: {}\n'.format(self.rentPerDay)
		s += 'minRentPeriodInDays: {}\n'.format(self.minRentPeriodInDays)
		s += 'fuelConsumptionPerDay: {}\n'.format(self.fuelConsumptionPerDay)
		s += 'landLot: {}\n'.format(self.landLot)
		return s

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


if __name__ == '__main__':

	aDrillingRig = DrillingRig()