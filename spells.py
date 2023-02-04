from ursina import *

"""
I couldn't use dict for this, since you can't define functions inside those.
However, this mess of classes will work. Under each combination, you can define
the possible spells for that combination. For this demo there's currently only
one Spell possible for each combination, since we probably won't have time to
make the spell randimization on startup feature, nor make enough spells in time.
"""

class Spells:
# --------------------------------------------------------------------- level 1
    class Combination_100:
        class Photon:
            description = 'Deal 4 damage'
            def use(enemy, player, battle):
                enemy.damage(4 + player.total_strength())

    class Combination_010:
        class Seed:
            description = 'Deal 1 damage and heal 1 and Gain 1 Block'
            def use(enemy, player, battle):
                enemy.damage(1 + player.total_strength())
                player.heal(1)
                player.block += 1

    class Combination_001:
        class Droplet:
            description = 'Gain 3 Block'
            def use(enemy, player, battle):
                player.block += 3 + player.total_fortitude()
                print("Gain 3 Block")

# --------------------------------------------------------------------- level 2
    class Combination_200:
        class Ray:
            description = 'Deal 6 damage if enemy is below half health, otherwise deal 3'
            def use(enemy, player, battle):
                if enemy.hp + enemy.hp < enemy.max_hp:
                    enemy.damage(7 + player.total_strength())
                else:
                    enemy.damage(3 + player.total_strength())

            def get_description(enemy, player, battle):
                return f'Deal {6 + player.total_strength()} damage if enemy is below half health, otherwise deal 3'

    class Combination_110:
        class Mist:
            description = 'Deal 3 damage, then 2 Strength for the rest of this turn'
            def use(enemy, player, battle):
                enemy.damage(3 + player.total_strength())
                player.temp_strength += 2

    class Combination_020:
        class Root:
            description = 'Gain 1 Strength and Heal 1'
            def use(enemy, player, battle):
                player.strength += 1
                player.heal(1)

    class Combination_011:
        class Spring:
            description = 'Gain 4 Block'
            def use(enemy, player, battle):
                player.block += 5 + player.total_fortitude()

    class Combination_002:
        class Stream:
            description = 'Gain 2 Block, then 2 fortitude for the rest of this turn'
            def use(enemy, player, battle):
                player.block += 3 + player.total_fortitude()
                player.temp_fortitude += 2

    class Combination_101:
        class Spark:
            description = 'Deal 1 damage 2 times'
            def use(enemy, player, battle):
                enemy.damage(1 + player.total_strength())
                enemy.damage(1 + player.total_strength())

# --------------------------------------------------------------------- level 3
    class Combination_300:
        class Light:
            description = 'Deal 1 damage for each Orb in Discard'
            def use(enemy, player, battle):
                enemy.damage(len(battle.discard) + player.total_strength())

    class Combination_201:
        class Rainbow:
            description = 'Draw 1 orb, then deal 1 damage for each Orb in Hand'
            def use(enemy, player, battle):
                battle.draw_orbs(1)

    class Combination_210:
        class Desert:
            description = 'Lose 2 Block and gain 2 Actions'
            def use(enemy, player, battle):
                if (player.block >= 2):
                    player.block -= 2
                    BATTLE.actions_left += 2

    class Combination_030:
        class Earth:
            description = 'Deal 1 damage for each Block you have'
            def use(enemy, player, battle):
                enemy.damage(player.block + player.total_strength)

    class Combination_120:
        class Volcano:
            description = 'Deal ?? damage'
            def use(enemy, player, battle):
                enemy.hp -= 10

    class Combination_021:
        class Storm:
            description = 'Deal ?? damage'
            def use(enemy, player, battle):
                enemy.hp -= 10

    class Combination_003:
        class Water:
            description = 'Gain 6 Block'
            def use(enemy, player, battle):
                player.block += 6 + player.total_fortitude()


    class Combination_102:
        class Lightning:
            description = 'Deal 3 damage and gain 1 Action'
            def use(enemy, player, battle):
                enemy.damage(3 + player.total_strength())
                battle.actions_left += 1


    class Combination_012:
        class Flood:
            description = 'Gain 1 Block twice, then gain 1 Fortitude'
            def use(enemy, player, battle):
                player.block += 1 + player.total_fortitude()
                player.block += 1 + player.total_fortitude()
                player.fortitude += 1

    class Combination_111:
        class Life:
            description = 'Deal ?? damage'
            def use(enemy, player, battle):
                enemy.hp -= 10


def get_spell_for_combination(combination=[1,0,0]):
    combo = Spells.__dict__[f'Combination_{combination[0]}{combination[1]}{combination[2]}']
    spell = [value for (key,value) in combo.__dict__.items() if not key.startswith('_')][0]
    return spell

rarity_colors = ['white', 'lime', 'gold']

from draggable_orb import DraggableOrb
class SpellTree(Entity):
    def __init__(self, enabled=False, **kwargs):
        super().__init__(parent=camera.ui, enabled=enabled, **kwargs)
        self.bg = Sprite('shore', parent=self, ppu=1080, color=hsv(0,0,0,.8), z=100)

        combinations = [value for (key,value) in Spells.__dict__.items() if key.startswith('Combination_')]
        # print(combinations)
        orb_parent = Entity(parent=self, scale=.1, y=.25)
        layers = [Entity(parent=orb_parent, y=-i*2) for i in range(3)]

        for y, combo in enumerate(combinations):
            level = sum([int(e) for e in combo.__name__[-3:]])
            print(f'{combo.__name__}  (lvl: {level})')
            orb = DraggableOrb([int(e) for e in combo.__name__[-3:]], parent=layers[level-1], ignore=True)
            orb.tooltip.text = ''

            spells = [value for (key,value) in combo.__dict__.items() if not key.startswith('_')]
            for s in spells:
                print(' ', s.__name__)
                orb.tooltip.text += f'<{rarity_colors[level-1]}>{s.__name__}\n'
                orb.tooltip.text += f'<scale:.75>{s.description}'

            orb.tooltip.create_background()

        for e in layers:
            grid_layout(e.children, origin=(0,0,0), max_x=10)



if __name__ == '__main__':
    app = Ursina()
    st = SpellTree(enabled=True)

    EditorCamera()
    app.run()
