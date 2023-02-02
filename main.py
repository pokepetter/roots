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

class OverworldEnemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(model='wireframe_cube', collider='box', color=color.magenta, trigger_targets=[player, ], **kwargs)

    def update(self):
        if self.intersects(player):
            self.enabled = False
            camera.animate('z', -7, duration=.4)
            camera.overlay.animate_color(color.black, duration=.4)
            invoke(Func(enter_battle, self), delay=.4)


test_enemy = OverworldEnemy(position=(-3,0,4))

import battle   # importing this creates global BATTLE


def enter_battle(enemy=test_enemy):
    print('enter battle')
    camera.overlay.animate_color(color.clear, duration=.4)
    BATTLE.enabled = True


def input(key):
    if key == 'space':
        player.position = test_enemy.position




app.run()
