class Orb():

    def __init__(self, name, mistCount, lightCount, seedCount, effect, **kwargs):
        self.name = name
        self.mistCount = mistCount
        self.lightCount = lightCount
        self.seedCount = seedCount
        self.effect = effect

    def getName(self):
        return self.name

    def getMistCount(self):
        return self.mistCount
    
    def getLightCount(self):
        return self.mistCount

    def getSeedCount(self):
        return  self.mistCount

    def getSpecialType(self):
        return  self.effect