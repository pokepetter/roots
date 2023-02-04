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

        self.block_bar = HealthBar(max_value=30, parent=self, y=-.45, scale=(.75,.045/3), color=color.clear, bar_color=hsv(0,0,1,.5), z=-1, show_text=False, show_lines=True, highlight_color=color.clear)
        self.block_bar.x = -self.health_bar.scale_x / 2
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
        self.player_ui = Entity(parent=self, position=(-(self.max_orbs/2*.1),-.4), scale=.1)
        self.orb_parent = Entity(parent=self.player_ui)
        self.orb_panel = Entity(parent=self.player_ui, model='quad', texture='white_cube', color=color.light_gray, scale=(self.max_orbs,1), texture_scale=(self.max_orbs,1), z=1, origin_x=-.5)

        self.bag_icon = Button(parent=self.player_ui, icon='bag', x=self.max_orbs+1, collider=None)
        for i in range(15): # max bag size
            orb = DraggableOrb(parent=self.bag_icon, scale=.5, ignore=True)
        grid_layout(self.bag_icon.children, max_x=5, origin=(0,0), offset=(0,1))


        from spell_tree import SpellTree
        spell_tree = SpellTree()
        self.spell_tree_button = Button(parent=self.player_ui, icon='rainbow', x=self.max_orbs+2.5, on_click=spell_tree.enable)
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
        [e.disable() for e in self.bag_icon.children]
        for i, orb_type in enumerate(value):
            self.bag_icon.children[i].enabled = True
            self.bag_icon.children[i].orb_type = orb_type


    def draw_orbs(self, amount):
        amount = min(amount, len(self.bag))

        orb_types_drawn = self.bag[:amount] # get copy of top 5
        self.bag = self.bag[amount:]    # remove top 5

        for i, orb_type in enumerate(orb_types_drawn):
            d = DraggableOrb(orb_type, parent=self.orb_parent, x=7)
            d.orb_type = orb_type
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
