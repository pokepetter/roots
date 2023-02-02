class Strike:
    description = 'Deal 4 damage'
    tier = 1

    @staticmethod
    def use(enemy, player):
        enemy.health -= 4
        print('Deal 4 damage')

class Block:
    description = 'Gain 3 Block'
    tier = 1

    @staticmethod
    def use(enemy, player):
        player.block += 3
        print("Gain 3 Block")

class Drain:
    description = 'Deal 2 damage and heal 1'
    tier = 1

    @staticmethod
    def use(enemy, player):
        enemy.health -= 2
        player.health += 1
        print("Heal 2")

if __name__ == '__main__':
    from ursina import *
    from main import DraggableOrb
    app = Ursina()

    app.run()
