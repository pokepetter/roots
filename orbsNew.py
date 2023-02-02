class Orb:
    description = ''
    
    @staticmethod
    def use(enemy, player):
        print('Used orb')

class PhotonOrb(Orb):
    description = ''
    photon = 1
    seed = 0
    droplet = 0

    @staticmethod
    def use(enemy, player):
        print('Used orb')

class SeedOrb(Orb):
    description = ''
    photon = 0
    seed = 1
    droplet = 0


    @staticmethod
    def use(enemy, player):
        print('Used orb')

class DropletOrb(Orb):
    description = ''
    photon = 0
    seed = 0
    droplet = 1


    @staticmethod
    def use(enemy, player):
        print('Used orb')

class RayOrb(Orb):
    description = ''
    photon = 2
    seed = 0
    droplet = 0


    @staticmethod
    def use(enemy, player):
        print('Used orb')

class RootOrb(Orb):
    description = ''
    photon = 0
    seed = 2
    droplet = 0


    @staticmethod
    def use(enemy, player):
        print('Used orb')

class StreamOrb(Orb):
    description = ''
    photon = 0
    seed = 0
    droplet = 2


    @staticmethod
    def use(enemy, player):
        print('Used orb')

class SpringOrb(Orb):
    description = ''
    photon = 1
    seed = 1
    droplet = 0


    @staticmethod
    def use(enemy, player):
        print('Used orb')

class SparkOrb(Orb):
    description = ''
    photon = 1
    seed = 0
    droplet = 1


    @staticmethod
    def use(enemy, player):
        print('Used orb')

class MistOrb(Orb):
    description = ''
    photon = 0
    seed = 1
    droplet = 1


    @staticmethod
    def use(enemy, player):
        print('Used orb')

class LightOrb(Orb):
    description = ''
    photon = 3
    seed = 0
    droplet = 0

    @staticmethod
    def use(enemy, player):
        print('Used orb')

class EarthOrb(Orb):
    description = ''
    photon = 0
    seed = 3
    droplet = 0

    @staticmethod
    def use(enemy, player):
        print('Used orb')

class WaterOrb(Orb):
    description = ''
    photon = 0
    seed = 0
    droplet = 3

    @staticmethod
    def use(enemy, player):
        print('Used orb')

class DesertOrb(Orb):
    description = ''
    photon = 3
    seed = 1
    droplet = 0

    @staticmethod
    def use(enemy, player):
        print('Used orb')

class LightningOrb(Orb):
    description = ''
    photon = 1
    seed = 0
    droplet = 2

    @staticmethod
    def use(enemy, player):
        print('Used orb')

class StormOrb(Orb):
    description = ''
    photon = 0
    seed = 2
    droplet = 1

    @staticmethod
    def use(enemy, player):
        print('Used orb')

class VolcanoOrb(Orb):
    description = ''
    photon = 1
    seed = 2
    droplet = 0

    @staticmethod
    def use(enemy, player):
        print('Used orb')

class IceOrb(Orb):
    description = ''
    photon = 0
    seed = 1
    droplet = 2

    @staticmethod
    def use(enemy, player):
        print('Used orb')

class RainbowOrb(Orb):
    description = ''
    photon = 2
    seed = 0
    droplet = 1

    @staticmethod
    def use(enemy, player):
        print('Used orb')

class LifeOrb(Orb):
    description = ''
    photon = 1
    seed = 1
    droplet = 1

    @staticmethod
    def use(enemy, player):
        print('Used orb')

def mergeOrbs(orbFirst, orbSecond):
    photon = orbFirst.photon + orbSecond.photon
    seed = orbFirst.seed + orbSecond.seed
    droplet = orbFirst.droplet + orbSecond.droplet

    if (photon == 2 and seed == 0 and droplet == 0): return RayOrb
    if (photon == 0 and seed == 2 and droplet == 0): return RootOrb
    if (photon == 2 and seed == 0 and droplet == 2): return StreamOrb
    if (photon == 1 and seed == 1 and droplet == 0): return SpringOrb
    if (photon == 0 and seed == 1 and droplet == 1): return SparkOrb
    if (photon == 1 and seed == 0 and droplet == 1): return MistOrb
    if (photon == 3 and seed == 0 and droplet == 0): return LightOrb
    if (photon == 0 and seed == 3 and droplet == 0): return EarthOrb
    if (photon == 0 and seed == 0 and droplet == 3): return WaterOrb
    if (photon == 2 and seed == 1 and droplet == 0): return DesertOrb
    if (photon == 2 and seed == 0 and droplet == 1): return RainbowOrb
    if (photon == 0 and seed == 2 and droplet == 1): return StormOrb
    if (photon == 0 and seed == 1 and droplet == 2): return IceOrb
    if (photon == 1 and seed == 0 and droplet == 2): return RainbowOrb
    if (photon == 1 and seed == 2 and droplet == 0): return VolcanoOrb   
    if (photon == 1 and seed == 2 and droplet == 0): return LifeOrb
    else: return None

if __name__ == '__main__':
    from ursina import *
    from main import DraggableOrb
    app = Ursina()

    app.run()
