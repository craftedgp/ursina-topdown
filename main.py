from ursina import *
from direct.actor.Actor import Actor
from ursina.shaders import lit_with_shadows_shader, fxaa_shader

app = Ursina(title='PTXO', fullscreen=True, show_ursina_splash=True)

version = Text('PTXO Alpha-0.0.2', color=color.white, position=window.top_left, scale=1)
# ======= <Top Down Controller> =======
mouse.visible = False
idle_animation = Actor('assets/animations/player/idle_combat.gltf')
idle_animation.loop('UE4_Mannequin_Skeleton|UE4_Mannequin_Skeleton|Combat_Idle')
sprint_actor = Actor('assets/animations/player/sprint.gltf')
sprint_actor.loop('UE4_Mannequin_Skeleton|UE4_Mannequin_Skeleton|Sprint')
player = Entity(model=idle_animation, collider='box', position=(0, 0, 0))
crosshair = Entity(model='quad', texture='assets/gfx/crosshair.png', parent=camera.ui, scale=(.1, .1), position=(0, 0, 2))
camera.rotation_x = 90
# ======= </Top Down Controller> ======

# ======= <Raycast Collision Handling> =======
def move_with_raycast(direction):
    speed = 8 * time.dt
    ray = raycast(player.world_position, direction, ignore=(player,), distance=0.5, debug=True)
    if not ray.hit:
        player.position += direction * speed
# ======= </Raycast Collision Handling> ========

# ======= <MAP LAYOUT> =======
camera.shader = fxaa_shader
Sky()
Entity.default_shader = lit_with_shadows_shader
directional_light = DirectionalLight(shadow=True)
directional_light.look_at(Vec3(1, -1, -1))
the_giant_floor = Entity(model='cube', texture='brick', texture_scale=(50, 50), collider='box', scale=(50, .5, 50), position=(-1, -1, -1))
block = Entity(model='cube', collider='box', position=(3, 0, 0), color=color.red)
# hallway = Entity(model='assets/maps/hallway.gltf', collider='mesh', position=(0, -1, 0))
# ======= </MAP LAYOUT> ======

# ======= <UPDATE AND INPUT FUNCTION FOR EVERYTHING> =======
def update():
    # ---- <Correct broken animations> ----
    idle_animation.setHpr(180, 0, 0)
    sprint_actor.setHpr(180, 0, 0)
    # ---- </Correct broken animations> ----
    # ---- <Update Crosshair and Player Position/Roation> ----
    camera.position = lerp(camera.position, (player.x, 20, player.z), 10 * time.dt)
    crosshair.position = mouse.position
    player.look_at_xz(Vec3(mouse.x + player.x, 0, mouse.y + player.z))
    # ---- </Update Crosshair and Player Position/Roation> ----
    # ---- <Controls> ----
    if held_keys['w']:
        move_with_raycast(Vec3(0, 0, 1))

    if held_keys['s']:
        move_with_raycast(Vec3(0, 0, -1))

    if held_keys['a']:
        move_with_raycast(Vec3(-1, 0, 0))

    if held_keys['d']:
        move_with_raycast(Vec3(1, 0, 0))
    # ---- </Controls> ----

def input(key):
    # ---- <Animation handling> ----
    if held_keys['w']:
        player.model = sprint_actor
    elif held_keys['s']:
        player.model = sprint_actor
    elif held_keys['a']:
        player.model = sprint_actor
    elif held_keys['d']:
        player.model = sprint_actor
    else:
        player.model = idle_animation
    # ---- </Animation handling> ----
# ======= </UPDATE AND INPUT FUNCTION FOR EVERYTHING> ======
app.run()
