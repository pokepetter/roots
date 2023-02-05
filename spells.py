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
                player.block += 1 + player.total_fortitude()

    class Combination_001:
        class Droplet:
            description = 'Gain 3 Block'
            def use(enemy, player, battle):
                player.block += 3 + player.total_fortitude()
                print("Gain 3 Block")

# --------------------------------------------------------------------- level 2
    class Combination_200:
        class Ray:
            description = 'Deal 2 damage twice'
            def use(enemy, player, battle):
                enemy.damage(2 + player.total_strength())
                enemy.damage(2 + player.total_strength())

    class Combination_110:
        class Mist:
            description = 'Deal 2 damage, then gain 3 Strength this turn'
            def use(enemy, player, battle):
                enemy.damage(2 + player.total_strength())
                player.temp_strength += 3

    class Combination_020:
        class Root:
            description = 'Gain 1 Strength and Heal 1'
            def use(enemy, player, battle):
                player.strength += 1
                player.heal(1)

    class Combination_011:
        class Spring:
            description = 'Deal 1 damage and Gain 4 Block'
            def use(enemy, player, battle):
                enemy.damage(1 + player.total_strength())
                player.block += 4 + player.total_fortitude()

    class Combination_002:
        class Stream:
            description = 'Gain 2 Block, then gain 3 fortitude this turn'
            def use(enemy, player, battle):
                player.block += 2 + player.total_fortitude()
                player.temp_fortitude += 3

    class Combination_101:
        class Spark:
            description = 'Deal 2 damage and gain 1 Action'
            def use(enemy, player, battle):
                enemy.damage(2 + player.total_strength())
                battle.actions_left += 1

# --------------------------------------------------------------------- level 3
    class Combination_300:
        class Light:
            description = 'Deal 1 damage twice then gain 1 Strength'
            def use(enemy, player, battle):
                enemy.damage(1 + player.total_strength())
                enemy.damage(1 + player.total_strength())
                player.strength += 1

    class Combination_201:
        class Rainbow:
            description = 'Draw 2 orbs, then deal 1 damage for each Orb in Hand'
            def use(enemy, player, battle):
                battle.draw_orbs(2)
                enemy.damage(len(battle.hand) + player.total_strength())

    class Combination_210:
        class Desert:
            description = 'Lose 2 Block and gain 2 Actions'
            def use(enemy, player, battle):
                if (player.block >= 2):
                    player.block -= 2
                    BATTLE.actions_left += 2

    class Combination_030:
        class Earth:
            description = 'Draw 2 orbs and Gain 1 Action'
            def use(enemy, player, battle):
                battle.draw_orbs(2)
                BATTLE.actions_left += 1

    class Combination_120:
        class Volcano:
            description = 'Deal 1 damage for each turn that has been, max 8'
            def use(enemy, player, battle):
                damage = battle.turn_count
                if (damage > 8):
                    damage = 8
                enemy.damage(damage + player.total_strength())

    class Combination_021:
        class Storm:
            description = 'Draw 2 orbs and gain 1 Fortitude'
            def use(enemy, player, battle):
                battle.draw_orbs(2)
                player.fortitude += 1

    class Combination_003:
        class Water:
            description = 'Gain 3 Block and gain 1 Action'
            def use(enemy, player, battle):
                player.block += 3 + player.total_fortitude()
                battle.actions_left += 1


    class Combination_102:
        class Lightning:
            description = 'Deal 1 damage, Gain 2 block and gain 1 Action'
            def use(enemy, player, battle):
                enemy.damage(1 + player.total_strength())
                player.block += 2 + player.total_fortitude()
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
            description = 'Gain 6 Block'
            def use(enemy, player, battle):
                player.block += 6 + player.total_fortitude()


def get_spell_for_combination(combination=[1,0,0]):
    combo = Spells.__dict__[f'Combination_{combination[0]}{combination[1]}{combination[2]}']
    spell = [value for (key,value) in combo.__dict__.items() if not key.startswith('_')][0]
    return spell

rarity_colors = ['white', 'lime', 'gold']
