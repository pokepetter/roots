

class FireOrb:
    description = 'Deal 50 damage. If enemy is below half health, deal +10 damage.'

    @staticmethod
    def use(enemy):
        enemy.hp -= 50
        if enemy.hp < enemy.max_hp/2:
            enemy.hp -= 10

        print('enemy hp:', enemy.hp)


class WaterOrb:
    description = 'Deal 5 damage. Heal self for +3'

    @staticmethod
    def use(enemy):
        enemy.hp -= 5
        if enemy.hp < enemy.max_hp/2:
            enemy.hp -= 10

        print('enemy hp:', enemy.hp)



if __name__ == '__main__':
    from ursina import *
    from main import DraggableOrb
    app = Ursina()

    app.run()
