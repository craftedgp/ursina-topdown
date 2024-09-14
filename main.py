from ursina import *
from direct.actor.Actor import Actor
from ursina.shaders import lit_with_shadows_shader

app = Ursina(title='PTXO', show_ursina_splash=True)
Sky()
Entity.default_shader = lit_with_shadows_shader
directional_light = DirectionalLight(shadow=True)
directional_light.look_at(Vec3(1, -1, -1))

# ======= <Top Down Controller> =======
mouse.visible = False
idle_animation = Actor('assets/animations/player/idle_combat.gltf')
idle_animation.loop('UE4_Mannequin_Skeleton|UE4_Mannequin_Skeleton|Combat_Idle')
sprint_actor = Actor('assets/animations/player/sprint.gltf')
sprint_actor.loop('UE4_Mannequin_Skeleton|UE4_Mannequin_Skeleton|Sprint')
player = Entity(model=idle_animation, collider='capsule', position=(0, 0, 0))
crosshair = Entity(model='quad', texture='assets/gfx/crosshair.png', parent=camera.ui, scale=(.1, .1), position=(0, 0, 2))
camera.rotation_x = 90
# ======= </Top Down Controller> ======

# ======= <MAP LAYOUT> =======
the_giant_floor = Entity(model='cube', texture='brick', texture_scale=(50, 50), collider='box', scale=(100, .5, 100), position=(-1, -1, -1))
# ======= </MAP LAYOUT> ======

# ======= <UPDATE AND INPUT FUNCTION FOR EVERYTHING> =======
def update():
    # ---- <Correct broken animations> ----
    idle_animation.setHpr(180, 0, 0)
    # ---- </Correct broken animations> ----
    # ---- <Update Crosshair and Player Position/Roation> ----
    camera.position = lerp(camera.position, (player.x, 10, player.z), 50 * time.dt)
    crosshair.position = mouse.position
    mouse_x = mouse.position.x * 20
    mouse_y = mouse.position.y * 20
    mouse_world_position = Vec3(mouse_x, 0, mouse_y) 
    player.look_at_xz(Vec3(mouse.x + player.x, 0, mouse.y + player.z))
    # ---- </Update Crosshair and Player Position/Roation> ----
    # ---- <Controls> ----
    speed = 8 * time.dt
    if held_keys['w']: 
        player.position += Vec3(0, 0, speed)

    if held_keys['s']: 
        player.position += Vec3(0, 0, -speed)

    if held_keys['a']: 
        player.position += Vec3(-speed, 0, 0)

    if held_keys['d']: 
        player.position += Vec3(speed, 0, 0)
    # ---- </Controls> ----

def input(key):
    # ---- <Animation handling> ----
    if held_keys['w']:
        sprint_actor.setHpr(180, 0, 0)
        player.model = sprint_actor
    elif held_keys['s']:
        sprint_actor.setHpr(180, 0, 0)
        player.model = sprint_actor
    elif held_keys['a']:
        sprint_actor.setHpr(180, 0, 0)
        player.model = sprint_actor
    elif held_keys['d']:
        sprint_actor.setHpr(180, 0, 0)
        player.model = sprint_actor
    else:
        player.model = idle_animation
        idle_animation.setHpr(180, 0, 0)
    # ---- </Animation handling> ----
# ======= </UPDATE AND INPUT FUNCTION FOR EVERYTHING> ======
app.run()
