from ursina import *
import builtins

from ursina.prefabs.health_bar import HealthBar
class Player(Entity):
    def __init__(self, max_health, **kwargs):
        super().__init__(**kwargs)
        self.health_bar = HealthBar(max_value=max_health, parent=self, y=-.45, scale=(.75,.045))
        self.health_bar.x = -self.health_bar.scale_x / 2
        self.max_hp = max_health
        self._hp = max_health
        self.hp = max_health

        self.block = 0
        self.strength = 0
        self.fortitude = 0
        self.temp_strength = 0
        self.temp_fortitude = 0
        self.orb_draw_count = 5
        self.orbs = self.create_starter_orbs()

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        value = clamp(value, 0, self.max_hp)
        self.health_bar.value = value

        if value <= 0:
            print('YOU DIED!')

        elif value > self.hp:
            print('HEAL :D')

        self._hp = value

    def damage(self, damage):
        damage_taken = damage - self.block
        if damage_taken < 0:
            damage_taken = 0
            self.block -= damage
        else:
            self.block = 0
        self.health_bar.value -= damage_taken
        self._hp -= damage_taken
        if self._hp <= 0:
            print('YOU DIED!')

    def heal(self, heal):
        self._hp += heal
        self.health_bar.value += heal
        if (self._hp > self.max_hp):
            self._hp = self.max_hp
            self.health_bar.value = self.max_hp

    def total_fortitude(self):
        return self.fortitude + self.temp_fortitude

    def total_strength(self):
        return self.strength + self.temp_strength

    def prepare_for_battle(self, battle):
        self.block = 0
        self.strength = 0
        self.fortitude = 0
        self.temp_strength = 0
        self.temp_fortitude = 0

    def prepare_for_new_turn(self, battle):
        self.block = 0
        self.temp_strength = 0
        self.temp_fortitude = 0

    def create_starter_orbs(self):
        orbs = []
        for i in range(5):
            orbs.append([1,0,0])
            orbs.append([0,1,0])
            orbs.append([0,0,1])
        return orbs

class Enemy(Entity):
    def __init__(self, max_health, **kwargs):
        super().__init__(model='quad', collider='box', scale=(.3,.3), color=color.white, texture='rutabaga', name='enemy', **kwargs)
        self.health_bar = HealthBar(max_value=max_health, scale_x=.2, world_parent=self, position=Vec3(-.1,.6,0))
        self.health_bar.x = -self.health_bar.scale_x / 2
        self.max_hp = max_health
        self._hp = max_health
        self.hp = max_health
        self.block = 0

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        print(f'set enemy hp from {self._hp} to {value}')
        value = clamp(value, 0, self.max_hp)
        self.health_bar.value = value

        if value < self._hp:
            print('ow!')
            self.blink(color.red, duration=.2)
            self.shake(duration=.2, magnitude=.03)

        if value <= 0:
            self.die()

        elif value > self._hp:
            print('heal enemy')

        self._hp = value

    def damage(self, damage):
        damage_taken = damage - self.block
        if damage_taken < 0:
            damage_taken = 0
            self.block -= damage
        else:
            self.block = 0
        self.health_bar.value -= damage_taken
        self._hp -= damage_taken
        if self._hp <= 0:
            self.die()

    def heal(self, heal):
        self._hp += heal
        self.health_bar.value += heal
        if (self._hp > self.max_hp):
            self._hp = self.max_hp
            self.health_bar.value = self.max_hp

    def die(self):
        BATTLE.enemies.remove(self)
        BATTLE.check_for_win()
        destroy(self, delay=.1)


from spells import get_spell_for_combination
import spells

orb_colors = [color.orange, color.lime, color.azure]
orb_shapes = ['quad', 'quad', 'circle']

class DraggableOrb(Draggable):
    def __init__(self, orb_type=[1,0,1], **kwargs):
        super().__init__(model='quad', color=color.brown, highlight_color=color.brown, texture='orb', **kwargs)
        self.sub_orbs = [Entity(parent=self, model='circle', z=-.001, scale=.25, color=hsv(20,.5,.25), position=pos) for pos in ((0,.2), (.15,-.1), (-.15,-.1))]
        self.tooltip = Tooltip('...')

        self.orb_type = orb_type


    def drag(self):
        self.start_position = self.position

    def drop(self):
        mouse.update()
        entities_under_mouse = [hit_info.entity for hit_info in mouse.collisions]
        targets = [e for e in entities_under_mouse if isinstance(e, (Enemy, DraggableOrb)) and not e == self]

        if not targets:
            self.position = self.start_position
            return


        target = targets[0]
        if isinstance(target, Enemy):
            print('USE ORB')
            self.spell.use(target, PLAYER, BATTLE)
            BATTLE.discard.append(self)
            BATTLE.hand.remove(self)
            destroy(self)
            BATTLE.actions_left -= 1
            BATTLE.reorder_orbs()
            return

        if isinstance(target, DraggableOrb):
            if BATTLE.actions_left <= 0:
                self.position = self.start_position
                return

            if sum(target.orb_type) == 3:   # can't combine with a complete orb
                print_on_screen('<red>ALREADY FULL', position=Vec3(mouse.position.xy, -10), origin=(0,-1))
                self.position = self.start_position
                return

            print('COMBINE ORBS')
            print_on_screen('COMBINE', position=Vec3(mouse.position.xy, -10), origin=(0,-1))
            new_orb_type = [sum(e) for e in zip(target.orb_type, self.orb_type)]
            target.orb_type = new_orb_type

            BATTLE.actions_left -= 1
            BATTLE.hand.remove(self)
            destroy(self)
            BATTLE.reorder_orbs()
            return


    @property
    def orb_type(self):
        return self._orb_type

    @orb_type.setter
    def orb_type(self, value):
        self._orb_type = value
        self.spell = get_spell_for_combination(value)

        level = sum(value)
        self.tooltip.text = f'<{spells.rarity_colors[level-1]}>{self.spell.__name__}\n<default>'
        self.tooltip.text += f'<scale:.75>{self.spell.description}'
        self.tooltip.create_background()

        n = 0
        for i, particle in enumerate(value):
            for j in range(particle):
                self.sub_orbs[n].color = orb_colors[i]
                # self.sub_orbs[n].model = copy(orb_shapes[i])
                n += 1

        self.scale = 1.5
        self.animate_scale(1, duration=.5)
        print('set orb type to:', value)



class Battle(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, enabled=False, **kwargs)
        self.bg = Entity(parent=self, model='quad', texture='shore', scale_x=16/9, z=10, color=color._32)
        self.win_screen = Text(parent=self, scale=7, text='VICTORY!', rotation_z=15, origin=(0,0), z=-2, enabled=False, target_scale=7)
        self.turn_count = 0

        self.enemies = [
            Enemy(parent=self, max_health=20, y=.1),
            ]
        self.player = Player(parent=self, max_health=20)
        builtins.PLAYER = self.player
        self.player.prepare_for_battle(self)

        self.max_actions = 3
        self.actions_left = self.max_actions
        self.actions_counter = Button(parent=self, scale=.1, text=f'<white>{self.actions_left} <gray>\nactions \nleft', y=-.25, color=color.violet)
        self.actions_counter.original_scale = self.actions_counter.scale

        self.max_orbs = 7
        self.orb_parent = Entity(parent=self, position=(-(self.max_orbs/2*.1),-.4), scale=.1)
        self.orb_panel = Entity(parent=self.orb_parent, model='quad', texture='white_cube', color=color.light_gray, scale=(self.max_orbs,1), texture_scale=(self.max_orbs,1), z=1, origin_x=-.5)

        self.bag_icon = Button(parent=self.orb_parent, icon='bag', x=8, collider=None)
        spell_tree = Entity()
        self.spell_tree_button = Button(parent=self.orb_parent, icon='rainbow', x=9.5, on_click=spell_tree.enable)
        self.fortitude_label = Button(parent=self.orb_parent, position=(2,1.25), text='fortitude:', tooltip=Tooltip('explain fortitude here'))
        self.strength_label =  Button(parent=self.orb_parent, position=(5,1.25), text='strength:', tooltip=Tooltip('explain strength here'))

        self.bag = self.player.orbs
        self.hand = []
        self.discard = []
        self.player_turn()


    def draw_orbs(self, amount):
        for i in range(amount):
            if (len(self.bag) == 0):
                self.bag.append(self.discard)
                self.discard.clear()
            if (len(self.hand) < self.max_orbs):
                orb = self.bag.pop()
                d = DraggableOrb(orb, parent=self.orb_parent, x=7)
                d.animate_x(i+.5)
                self.hand.append(d)
                self.reorder_orbs()
            else:
                return

    def on_enable(self):
        mouse.locked = False
        mouse.visible = True

    def reorder_orbs(self):
        self.actions_counter.text = f'<white>{self.actions_left} <gray>\nactions \nleft'

        for i, orb in enumerate(self.hand):
            orb.animate_x(i+.5, duration=abs(orb.x-(i+.5))*.1)

        if self.actions_left <= 0:
            for orb in self.hand:
                self.discard.append(orb.orb_type)
                destroy(orb)
            self.hand.clear()
            self.enemy_turn()

    def enemy_turn(self):
        print('enemy turn')
        for enemy in self.enemies:
            enemy.block = 0
        [setattr(e, 'ignore', True) for e in self.orb_parent.children]
        PLAYER.animate_position(Vec3(0,0,0), duration=.3, curve=curve.in_expo_boomerang)
        self.actions_counter.collision = False
        self.actions_counter.animate_scale_y(0)
        PLAYER.damage(5)        # damage player
        self.turn_count += 1
        invoke(self.player_turn, delay=1)

    def player_turn(self):
        print('player turn')
        self.player.prepare_for_new_turn(self)
        [setattr(e, 'ignore', False) for e in self.orb_parent.children]
        self.actions_counter.animate_scale_y(.1)
        self.actions_left = self.max_actions
        self.turn_count += 1
        self.draw_orbs(self.player.orb_draw_count)
        self.reorder_orbs()

    def check_for_win(self):
        if len(self.enemies) <= 0:
            print('VICTORY!!!')
            self.win_screen.enabled = True
            self.win_screen.scale = 4
            self.win_screen.animate_scale(self.win_screen.target_scale, duration=.4)
            self.win_screen.fade_out(duration=.4)
            camera.overlay.animate_color(color.black, duration=.8, delay=.5, curve=curve.in_out_expo_boomerang)
            invoke(self.disable, delay=.5+.4)

    def on_disable(self):
        camera.z = -15



if __name__ == '__main__':
    app = Ursina(forced_aspect_ratio=16/9)


builtins.BATTLE = Battle()


if __name__ == '__main__':
    BATTLE.enabled = True
    app.run()
