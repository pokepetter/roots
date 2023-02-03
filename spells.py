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
        class Strike:
            description = 'strike the enemy and deal 4 damage'
            def use(enemy, player):
                enemy.hp -= 4

    class Combination_010:
        class Block:
            description = 'Gain 3 Block'
            def use(enemy, player):
                player.block += 3
                print("Gain 3 Block")

    class Combination_001:
        class Drain:
            description = 'Deal 2 damage and heal 1'
            def use(enemy, player):
                enemy.hp -= 2
                player.hp += 1

# --------------------------------------------------------------------- level 2
    class Combination_200:
        class Ray:
            description = 'Deal 10 damage'
            def use(enemy, player):
                enemy.hp -= 10

    class Combination_110:
        class Mist:
            description = 'Deal 10 damage'
            def use(enemy, player):
                enemy.hp -= 10

    class Combination_020:
        class Root:
            description = 'Deal 10 damage'
            def use(enemy, player):
                enemy.hp -= 10

    class Combination_011:
        class Spring:
            description = 'Deal 10 damage'
            def use(enemy, player):
                enemy.hp -= 10

    class Combination_002:
        class Stream:
            description = 'Deal 10 damage'
            def use(enemy, player):
                enemy.hp -= 10

    class Combination_101:
        class Spark:
            description = 'Deal 10 damage'
            def use(enemy, player):
                enemy.hp -= 10

# --------------------------------------------------------------------- level 3
    class Combination_300:
        class Light:
            description = 'Deal ?? damage'
            def use(enemy, player):
                enemy.hp -= 10

    class Combination_201:
        class Rainbow:
            description = 'Deal ?? damage'
            def use(enemy, player):
                enemy.hp -= 10

    class Combination_210:
        class Desert:
            description = 'Deal ?? damage'
            def use(enemy, player):
                enemy.hp -= 10

    class Combination_030:
        class Earth:
            description = 'Deal ?? damage'
            def use(enemy, player):
                enemy.hp -= 10

    class Combination_120:
        class Volcano:
            description = 'Deal ?? damage'
            def use(enemy, player):
                enemy.hp -= 10

    class Combination_021:
        class Tsunami:
            description = 'Deal ?? damage'
            def use(enemy, player):
                enemy.hp -= 10

    class Combination_003:
        class Water:
            description = 'Deal ?? damage'
            def use(enemy, player):
                enemy.hp -= 10


    class Combination_102:
        class Lightning:
            description = 'Deal ?? damage'
            def use(enemy, player):
                enemy.hp -= 10


    class Combination_012:
        class Flood:
            description = 'Deal ?? damage'
            def use(enemy, player):
                enemy.hp -= 10

    class Combination_111:
        class Storm:
            description = 'Deal ?? damage'
            def use(enemy, player):
                enemy.hp -= 10


def get_spell_for_combination(combination=[1,0,0]):
    combo = Spells.__dict__[f'Combination_{combination[0]}{combination[1]}{combination[2]}']
    spell = [value for (key,value) in combo.__dict__.items() if not key.startswith('_')][0]
    return spell

rarity_colors = ['white', 'lime', 'gold']

if __name__ == '__main__':
    from ursina import *
    app = Ursina()
    Sprite('shore', parent=camera.ui, ppu=1080, color=color._32, z=100)
    from battle import DraggableOrb

    combinations = [value for (key,value) in Spells.__dict__.items() if key.startswith('Combination_')]
    # print(combinations)
    orb_parent = Entity(parent=camera.ui, scale=.1, y=.25)
    layers = [Entity(parent=orb_parent, y=-i*2) for i in range(3)]

    for y, combo in enumerate(combinations):
        level = sum([int(e) for e in combo.__name__[-3:]])
        print(f'{combo.__name__}  (lvl: {level})')
        orb = DraggableOrb([int(e) for e in combo.__name__[-3:]], parent=layers[level-1])
        orb.tooltip.text = ''

        spells = [value for (key,value) in combo.__dict__.items() if not key.startswith('_')]
        for s in spells:
            print(' ', s.__name__)
            orb.tooltip.text += f'<{rarity_colors[level-1]}>{s.__name__}\n'
            orb.tooltip.text += f'<scale:.75>{s.description}'

        orb.tooltip.create_background()

    for e in layers:
        grid_layout(e.children, origin=(0,0,0), max_x=10)

    EditorCamera()
    app.run()
