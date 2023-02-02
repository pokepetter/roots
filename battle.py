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
        super().__init__(model='quad', collider='box', scale=(.3,.3), color=color.white, texture='rutabaga', name='enemy', **kwargs)
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
class DraggableOrb(Draggable):
    def __init__(self, orb_type, **kwargs):
        super().__init__(**kwargs)
        self.orb_type = orb_type
        self.tooltip = Tooltip(orb_type.description)

    def drag(self):
        self.start_position = self.position

    def drop(self):
        mouse.update()
        entities_under_mouse = [hit_info.entity for hit_info in mouse.collisions]
        targets = [e for e in entities_under_mouse if isinstance(e, Enemy)]
        if not targets:
            targets = [] # TODO: add orb combining logic
            # target_combine_orb = [e for e in entities_under_mouse if not e==self and isintance(e, DraggableOrb)]
        if not targets:
            self.position = self.start_position
            return
        target = targets[0]
        print('----target:', target)
        if isinstance(target, Enemy):
            self.orb_type.use(target)
            print('USED ORB')
            destroy(self)
            BATTLE.actions_left -= 1
            BATTLE.reorder_orbs()


class Battle(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, enabled=False, **kwargs)
        self.bg = Entity(parent=self, model='quad', texture='shore', scale_x=16/9, z=10, color=color._32)
        self.enemies = [
            Enemy(parent=self, y=.1),
            ]
        builtins.PLAYER = Player(parent=self)

        self.max_actions = 3
        self.actions_left = self.max_actions
        self.actions_counter = Button(parent=self, scale=.1, text=f'<white>{self.actions_left} <gray>\nactions \nleft', y=-.25, color=color.violet)
        self.actions_counter.original_scale = self.actions_counter.scale

        self.orb_parent = Entity(parent=self, y=-.4, scale=.1)

        for i in range(5):
            d = DraggableOrb(FireOrb, parent=self.orb_parent, x=i)


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
            camera.overlay.animate_color(color.black, duration=.8, delay=.5, curve=curve.in_out_expo_boomerang)
            invoke(self.disable, delay=.5+.4)

    def on_disable(self):
        camera.z = -15



if __name__ == '__main__':
    app = Ursina(size=Vec2(1920*.25,1080*.25), borderless=True)


builtins.BATTLE = Battle()


if __name__ == '__main__':
    BATTLE.enabled = True
    app.run()
