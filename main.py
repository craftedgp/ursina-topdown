from ursina import *
from direct.actor.Actor import Actor
from ursina.shaders import lit_with_shadows_shader, fxaa_shader, ssao_shader

# ======= <CONFIG> =======

# ======= </CONFIG> =======

app = Ursina(title='PTXO', fullscreen=True, borderless=False, show_ursina_splash=True)

# ======= <Top Down Controller> =======
mouse.visible = False
idle_animation = Actor('assets/animations/player/idle_combat.gltf')
idle_animation.loop('UE4_Mannequin_Skeleton|UE4_Mannequin_Skeleton|Combat_Idle')
sprint_actor = Actor('assets/animations/player/sprint.gltf')
sprint_actor.loop('UE4_Mannequin_Skeleton|UE4_Mannequin_Skeleton|Sprint')
player = Entity(model=idle_animation, collider='box', position=(0, 100, 0))
crosshair = Entity(model='quad', texture='assets/gfx/crosshair.png', parent=camera.ui, scale=(.1, .1), position=(0, 0, 2), visible=True)
camera.rotation_x = 90
in_game = True
# ======= </Top Down Controller> ======

# ======= <Raycast Collision Handling and Gravity> =======
def move_with_raycast(direction):
    speed = 8 * time.dt
    ray = raycast(player.world_position, 
                  direction, 
                  ignore=(player,), 
                  distance=0.5, debug=True)
    
    if not ray.hit:
        player.position += direction * speed

gravity_force = 9.8
is_grounded = False
fall_speed = 0
max_fall_speed = 100

def apply_gravity():
    global fall_speed
    gravity_ray = raycast(player.world_position, 
                          Vec3(0, -1, 0), 
                          ignore=(player,), 
                          distance=1/2, 
                          debug=True)

    if not gravity_ray.hit:
        fall_speed = min(fall_speed + gravity_force * time.dt, max_fall_speed)
        below_player_ray = raycast(player.world_position + Vec3(0, -0.5, 0), Vec3(0, -1, 0), ignore=(player,), distance=fall_speed * time.dt, debug=True)
        if not below_player_ray.hit:
            player.y -= fall_speed * time.dt
    else:
        fall_speed = 0
# ======= </Raycast Collision Handling and Gravity> ========

# ======= <MAP LAYOUT> =======
# camera.shader = fxaa_shader
# camera.shader = ssao_shader
Sky()
Entity.default_shader = lit_with_shadows_shader
directional_light = DirectionalLight(shadow=True)
directional_light.look_at(Vec3(1, -1, -1))
the_giant_floor = Entity(model='cube', texture='brick', texture_scale=(50, 50), collider='box', scale=(50, .5, 50), position=(-1, -1, -1))
block = Entity(model='cube', collider='box', position=(3, 0, 0), color=color.red)
block2 = Entity(model='cube', collider='box', position=(-3, 0, 0), color=color.gray)
block3 = Entity(model='sphere', collider='sphere', position=(6, 0, 1), color=color.blue)
# hallway = Entity(model='assets/maps/hallway.gltf', position=(0, 0, 0))
stairs1 = Entity(model='assets/maps/stairs1.gltf', position=(10, 0, 10), collider='mesh')
# ======= </MAP LAYOUT> ======

# ======= <UI> =======
# ---- <Start Screen> ----
controls_font = 'assets/fonts/Exo2-Regular.ttf'
title_controls = Text('Controls', color=color.white66, position=(-.47, .25), origin=(0, 0), scale=2, font='assets/fonts/zekton rg.otf')
frame = Entity(model='wireframe_cube', color=color.white33, position=(-.47, -.03), scale=(.4, .5), parent=camera.ui)
walk_controls = Text('W, A, S, D', position=(-.47, .1), origin=(0, 0), font=controls_font)
rightclick_control = Text('Right Click : Pickup/Throw weapons', position=(-.47, 0), origin=(0, 0), font=controls_font, scale=0.9)
leftclick_control = Text('Left Click : Shoot/Melee', position=(-.47, -.1), origin=(0, 0), font=controls_font)
swipe_control = Text('Swipe Mouse : Curve bullets', position=(-.47, -.2), origin=(0, 0), font=controls_font)
controls_list = [title_controls, frame, walk_controls, rightclick_control, leftclick_control, swipe_control]
for i in controls_list:
    invoke(i.fade_out(duration=10))
# ---- </Start Screen> ----

# ---- <Button Commands> ----
def options():
    global in_options, placeholder, btn_back
    in_options = True
    def back():
        global in_options
        in_options = False
        destroy(placeholder)
        destroy(btn_back)
        resume_text.visible = True
        btn_options.visible = True
        btn_options.disabled = False
        btn_quit.visible = True
        btn_quit.disabled = False
        
    resume_text.visible = False
    btn_options.visible = False
    btn_options.disabled = True
    btn_quit.visible = False
    btn_quit.disabled = True
    placeholder = Text('Comming soon', color=color.red, position=(0, .2), origin=(0, 0), scale=1.5, font='assets/fonts/Exo-Regular.ttf')
    btn_back = Button(text='Back', position=(0, 0), origin=(0, 0), scale=(0.2, 0.05), on_click=back)
# ---- </Button Commands> ----
version = Text('PTXO Alpha-0.0.4', color=color.white, position=window.top_left, scale=1)
bg = Panel(origin=(0, 0), position=(0, 0), alpha=0.5, visible=False)
bg.scale_x = camera.aspect_ratio
bg.scale_y = camera.aspect_ratio
resume_text = Text('Press ESC again to resume', color=color.white, position=(0, 0.3), origin=(0, 0), scale=1.5, font='assets/fonts/zekton rg.otf', visible=False)
btn_options = Button(text='Options', origin=(0, 0), position=(0, -0.1), scale=(0.2, 0.05), disabled=True, visible=False, on_click=options)
btn_quit = Button(text='Quit', origin=(0, 0), position=(0, -0.2), scale=(0.2, 0.05), disabled=True, visible=False, on_click=application.quit)
# ======= </UI> =======

# ======= <UPDATE AND INPUT FUNCTION FOR EVERYTHING> =======
def update():
    # ---- <Gravity> ----
    apply_gravity()
    # ---- </Gravity> ----
    # ---- <Correct broken animations> ----
    idle_animation.setHpr(180, 0, 0)
    sprint_actor.setHpr(180, 0, 0)
    # ---- </Correct broken animations> ----
    # ---- <Update Crosshair and Player Position/Roation> ----
    camera.position = lerp(camera.position, (player.x, player.y + 20, player.z), 10 * time.dt)
    crosshair.position = mouse.position
    player.look_at_xz(Vec3(mouse.x + player.x, 0, mouse.y + player.z))
    # ---- </Update Crosshair and Player Position/Roation> ----
    # ---- <Controls> ----
    if in_game:
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
    # ---- <Pause Menu> ----
    global in_game
    if key == 'escape':
        in_game = not in_game
        if not in_game:
            crosshair.visible = False
            mouse.visible = True
            bg.visible = True
            resume_text.visible = True
            btn_options.disabled = False
            btn_options.visible = True
            btn_quit.disabled = False
            btn_quit.visible = True
        elif in_game:
            if in_options:
                destroy(placeholder)
                destroy(btn_back)
                resume_text.visible = True
                btn_options.visible = True
                btn_options.disabled = False
                btn_quit.visible = True
                btn_quit.disabled = False
            crosshair.visible = True
            mouse.visible = False
            bg.visible = False
            btn_options.disabled = True
            btn_options.visible = False
            resume_text.visible = False
            btn_quit.disabled = True
            btn_quit.visible = False
    # ---- </Pause Menu> ----

    # ---- <Animation handling> ----
    if in_game:
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
