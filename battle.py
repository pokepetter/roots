from ursina import *
import builtins

from ursina.prefabs.health_bar import HealthBar
class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.health_bar = HealthBar(parent=self, y=-.45, scale=(.75,.045))
        self.health_bar.x = -self.health_bar.scale_x / 2
        self.max_hp = 100
        self._hp = self.max_hp
        self.hp = self.max_hp

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


class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(model='quad', collider='box', scale=(.3,.3), color=color.white, texture='knot', name='enemy', **kwargs)
        self.health_bar = HealthBar(scale_x=.2, world_parent=self, position=Vec3(-.1,.6,0))
        self.health_bar.x = -self.health_bar.scale_x / 2
        self.max_hp = 100
        self._hp = self.max_hp
        self.hp = self.max_hp

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
            BATTLE.enemies.remove(self)
            BATTLE.check_for_win()
            destroy(self, delay=.1)

        elif value > self._hp:
            print('heal enemy')

        self._hp = value


from orbs import *
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
            self.spell.use(target, PLAYER)
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

        self.enemies = [
            Enemy(parent=self, y=.1),
            ]
        builtins.PLAYER = Player(parent=self)

        self.max_actions = 3
        self.actions_left = self.max_actions
        self.actions_counter = Button(parent=self, scale=.1, text=f'<white>{self.actions_left} <gray>\nactions \nleft', y=-.25, color=color.violet)
        self.actions_counter.original_scale = self.actions_counter.scale

        max_orbs = 7
        self.orb_parent = Entity(parent=self, position=(-(max_orbs/2*.1),-.4), scale=.1)
        self.orb_panel = Entity(parent=self.orb_parent, model='quad', texture='white_cube', color=color.light_gray, scale=(max_orbs,1), texture_scale=(max_orbs,1), z=1, origin_x=-.5)

        for i in range(5):
            orb_type = [0,0,0]
            for j in range(1):
                orb_type[random.randint(0,2)] += 1

            d = DraggableOrb(orb_type, parent=self.orb_parent, x=i+.5)


    def on_enable(self):
        mouse.locked = False
        mouse.visible = True


    def reorder_orbs(self):
        self.actions_counter.text = f'<white>{self.actions_left} <gray>\nactions \nleft'
        if self.actions_left <= 0:
            self.enemy_turn()


    def enemy_turn(self):
        print('enemy turn')
        [setattr(e, 'ignore', True) for e in self.orb_parent.children]
        PLAYER.animate_position(Vec3(0,0,0), duration=.3, curve=curve.in_expo_boomerang)
        self.actions_counter.collision = False
        self.actions_counter.animate_scale_y(0)
        PLAYER.hp -= 10        # damage player
        invoke(self.player_turn, delay=1)

    def player_turn(self):
        print('player turn')
        [setattr(e, 'ignore', False) for e in self.orb_parent.children]
        self.actions_counter.animate_scale_y(.1)
        self.actions_left = self.max_actions
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
