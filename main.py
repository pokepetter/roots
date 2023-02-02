from ursina import *


app = Ursina(forced_aspect_ratio=16/9)

window.color = color.black
level = load_blender_scene('overgrown_temple',
    reload=False,
    normals=False,
    uvs=False,
    decimals=2
    )
# for name, mesh in level.meshes.items():
#     print(name, mesh)
#     for i, col in enumerate(mesh.colors):
#         if Color(*col).v < .1:
#             mesh.colors[i] = lerp(col, color.azure.tint(-.7), .3)
#     mesh.generate()


class ThirdPersonController(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.speed = 5
        self.shadow = Entity(parent=self, model='plane', texture='radial_gradient', scale=1, y=.005, color=color.black)
        camera.z = -15
        camera.fov = 90
        self.camera_parent = EditorCamera(rotation=(35,0,0), move_speed=0, pan_speed=(0,0), rotate_key='rotate_key', ignore=True)
        self.camera_offset = Vec3(0,1,0)
        self.camera_smoothing = 10

        mouse.locked = True
        mouse.visible = False

        self.graphics = Entity(parent=self)
        self.animator = Animator({
            'run' :  Entity(model='cube', fps=16/2.083, texture='white_cube', parent=self.graphics),
            'idle' : Entity(model='cube', texture='white_cube', parent=self.graphics),
        })
        self.collider = 'box'

        for key, value in kwargs.items():
            setattr(self, key, value)


    def update(self):
        h = max((held_keys['gamepad left stick x'], held_keys['d']-held_keys['a']), key=lambda x: abs(x))
        v = max((held_keys['gamepad left stick y'], held_keys['w']-held_keys['s']), key=lambda x: abs(x))
        direction = Vec3(h,0,v)
        self.current_speed = min(direction.length(), 1)

        if self.current_speed:
            self.look_at_2d(self.position+direction, 'y')
            self.animator.state = 'run'
        else:
            self.animator.state = 'idle'

        self.position += self.forward * time.dt * self.speed * self.current_speed
        self.camera_parent.position = lerp(self.camera_parent.position, self.position + self.camera_offset, time.dt*self.camera_smoothing)


player = ThirdPersonController()
from ursina.trigger import Trigger

class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(model='wireframe_cube', collider='box', color=color.magenta, trigger_targets=[player, ], **kwargs)


    def update(self):
        if self.intersects(player):
            self.enabled = False
            camera.animate('z', -7, duration=.4)
            camera.overlay.animate_color(color.black, duration=.4)
            invoke(Func(enter_battle, self), delay=.4)


test_enemy = Enemy(position=(-3,0,4))
from ursina.prefabs.health_bar import HealthBar
class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.health_bar = HealthBar(parent=self, y=-.45, scale=(.75,.045))
        self.health_bar.x = -self.health_bar.scale_x / 2
        self.hp = 100

    @property
    def hp(self):
        return self._hp

    def set_hp(self, value):
        value = clamp(value, 0, 100)
        self._hp = value
        self.health_bar.value = value
        if value >= 0:
            print('YOU DIED!')


class Battle(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, enabled=0, **kwargs)
        self.bg = Entity(parent=self, model='quad', texture='shore', scale_x=16/9, z=10, color=color._32)
        self.enemy = Button(parent=self, model='quad', scale=(.3,.3), color=color.white, texture='rutabaga', y=.1, collision='box', name='enemy')
        self.enemy.health_bar = HealthBar(parent=self, position=self.enemy.position + Vec3(-.1,.2,0), scale_x=.2)
        self.player = Player(parent=self)

        self.actions_left = 3
        self.actions_counter = Button(parent=self, scale=.1, text=f'<white>{self.actions_left} <gray>\nactions \nleft', y=-.3, color=color.violet)
        self.orb_parent = Entity(parent=self, y=-.4, scale=.1)

        for i in range(5):
            d = Draggable(parent=self.orb_parent, x=i)
            def drop(d=d):
                mouse.update()
                print('--', [hit_info.entity.name for hit_info in mouse.collisions])
                if self.enemy in [hit_info.entity for hit_info in mouse.collisions]:
                    self.enemy.health_bar.value -= 10
                    destroy(d)
                    self.reorder_orbs()

            d.drop = drop

    def reorder_orbs(self):
        print('aaoiwdjawoidj')

        self.actions_counter.text = f'<white>{self.actions_left} <gray>actions left'
        if self.actions_left <= 0:
            self.enemy_turn()


    def enemy_turn(self):
        print('enemy turn')
        [setattr(e, 'ignore', True) for e in self.orb_parent.children]
        self.player.animate_position(Vec3(0,0,0), duration=.3, curve=curve.in_expo_boomerang)
        # invoke(self.player.set_hp(self.))

    def player_turn(self):
        print('player turn')
        [setattr(e, 'ignore', False) for e in self.orb_parent.children]

    def on_enable(self):
        mouse.locked = False
        mouse.visible = True


battle = Battle()


def enter_battle(enemy=test_enemy):
    print('enter battle')
    camera.overlay.animate_color(color.clear, duration=.4)
    battle.enabled = True



def input(key):
    if key == 'space':
        player.position = test_enemy.position




# orb_types = ['leaf', 'mist', 'earth', 'light']
#
# orb_parent = Entity(parent=camera.ui, x=-.5)
# def draw_orb():
#     orb = Draggable(parent=orb_parent, scale=.1, icon='orb', color=color.random_color(), )
#     grid_layout(orb_parent.children, spacing=[.05,.05,1])
#
#
# def input(key):
#     if key == 'space':
#         for i in range(10):
#             invoke(draw_orb, delay=i*.1)



app.run()
