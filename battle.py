from ursina import *
import builtins

from ursina.prefabs.health_bar import HealthBar
class Player(Entity):
    def __init__(self, max_health, **kwargs):
        super().__init__(**kwargs)

        self.health_bar = HealthBar(max_value=max_health, parent=self, y=-.455, scale=(.75,.04), color='#221612', bar_color='#8e0e2c', text_color=color.light_gray)
        self.health_bar.x = -self.health_bar.scale_x / 2
        self.max_hp = max_health
        self._hp = max_health
        self.hp = max_health

        self.block_bar = HealthBar(max_value=30, parent=self, y=-.45, scale=(.75,.045/3), color=color.clear, bar_color=hsv(0,0,1,.5), z=-1, show_text=False, show_lines=True, highlight_color=color.clear)
        self.block_bar.x = -self.health_bar.scale_x / 2
        self.block = 2

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

    @property
    def block(self):
        return self._block
    @block.setter
    def block(self, value):
        self._block = value
        self.block_bar.value = value



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


from enemy import Enemy
from draggable_orb import DraggableOrb

class Battle(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, enabled=False, **kwargs)
        from ursina.prefabs.ursfx import ursfx
        builtins.ursfx = ursfx

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
        self.player_ui = Entity(parent=PLAYER, position=(-(self.max_orbs/2*.1),-.4), scale=.1)
        self.orb_parent = Entity(parent=self.player_ui)
        s = .22
        self.orb_panel = Entity(parent=PLAYER, model='quad', texture='skill_bar', origin_y=-.5, y=-.5, scale=(s*8,s), z=1)

        self.bag_icon = Entity(model='quad', parent=self.player_ui, texture='bag', x=self.max_orbs+1, collider='box', color=color.light_gray)
        self.bag_orb_parent = Entity(parent=self.bag_icon, enabled=False)
        self.bag_icon.on_mouse_enter = self.bag_orb_parent.enable
        self.bag_icon.on_mouse_exit = self.bag_orb_parent.disable

        for i in range(15): # max bag size
            orb = DraggableOrb(parent=self.bag_orb_parent, scale=.5, ignore=True)
        grid_layout(self.bag_orb_parent.children, max_x=5, origin=(0,0), offset=(0,1))


        from spell_tree import SpellTree
        spell_tree = SpellTree()
        self.spell_tree_button = Button(parent=self.player_ui, model='circle', scale=.75, texture='rainbow', x=self.max_orbs+2.5, color=color.light_gray, on_click=spell_tree.enable)
        self.fortitude_label = Button(parent=self.player_ui, position=(2,1.25), text='fortitude:', tooltip=Tooltip('explain fortitude here'))
        self.strength_label =  Button(parent=self.player_ui, position=(5,1.25), text='strength:', tooltip=Tooltip('explain strength here'))

        self.bag = self.player.orbs
        self.player_turn()


    @property
    def bag(self):
        return self._bag
    @bag.setter
    def bag(self, value):
        self._bag = value
        [e.disable() for e in self.bag_orb_parent.children]
        for i, orb_type in enumerate(value):
            self.bag_orb_parent.children[i].enabled = True
            self.bag_orb_parent.children[i].orb_type = orb_type


    def draw_orbs(self, amount):
        amount = min(amount, len(self.bag)-1)

        orb_types_drawn = self.bag[:amount] # get copy of top 5
        self.bag = self.bag[amount:]    # remove top 5

        for i, orb_type in enumerate(orb_types_drawn):
            d = DraggableOrb(orb_type, parent=self.orb_parent, x=7)
            d.animate_x(i+.5)

        self.reorder_orbs()

    def on_enable(self):
        mouse.locked = False
        mouse.visible = True

    def reorder_orbs(self):
        self.actions_counter.text = f'<white>{self.actions_left} <gray>\nactions \nleft'

        for i, orb in enumerate(self.orb_parent.children):
            orb.animate_x(i+.5, duration=abs(orb.x-(i+.5))*.1)

        if self.actions_left <= 0:
            for orb in self.orb_parent.children:
                self.bag.append(orb.orb_type)
                destroy(orb)
            self.enemy_turn()


    def enemy_turn(self):
        print('enemy turn')
        for enemy in self.enemies:
            enemy.block = 0
        [setattr(e, 'ignore', True) for e in self.orb_parent.children]
        # PLAYER.animate_position(Vec3(0,0,0), duration=.3, curve=curve.in_expo_boomerang)

        self.enemies[0].animate_position(lerp(self.enemies[0].position, (0,-.5), .1), duration=.3, curve=curve.in_expo_boomerang, delay=.5)
        invoke(ursfx, [(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.38, 0.73), (0.8, 0.0)], volume=0.75, wave='noise', pitch=-13, pitch_change=-10, speed=4, delay=.5)
        PLAYER.shake(delay=.65, magnitude=.05)
        self.actions_counter.collision = False
        self.actions_counter.animate_scale_y(0)
        PLAYER.damage(5)        # damage player
        self.turn_count += 1
        invoke(self.player_turn, delay=1.5)

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
