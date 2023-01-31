from ursina import *


app = Ursina(forced_aspect_ratio=16/9)

window.color = color.black
level = load_blender_scene('overgrown_temple',
    reload=True
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
        camera.z = -12
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


ThirdPersonController()



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
