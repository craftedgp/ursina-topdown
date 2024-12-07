# you can delete this :(
# =====   MADE BY  =====
# ====   CRAFTEDGP  ====
# ====     a.k.a    ====
# =====  _gamedev  =====


from ursina import *
from direct.actor.Actor import Actor
from ursina.shaders import lit_with_shadows_shader, fxaa_shader, ssao_shader

app = Ursina(title='Ursina TopDown Template', fullscreen=True, borderless=False, show_ursina_splash=True)

# ======= <Top Down Controller> =======
# ---- <Animations> ----
idle_animation = Actor('assets/animations/player/idle_gun.gltf')
idle_animation.loop('Armature|mixamo.com|Layer0')
sprint_animation = Actor('assets/animations/player/sprint.gltf')
sprint_animation.loop('Armature|mixamo.com|Layer0')
falling_unarmed_animation = Actor('assets/animations/player/falling_unarmed.gltf')
falling_unarmed_animation.loop('Armature|mixamo.com|Layer0')
# <Correct broken animations> 
idle_animation.setHpr(180, 0, 0)
sprint_animation.setHpr(180, 0, 0)
falling_unarmed_animation.setHpr(180, 0, 0)
# </Correct broken animations>
# ---- </Animations> ----
mouse.visible = False
player = Entity(model=idle_animation, position=(0, 100, 0))
equiped_gun = Entity(model='assets/items/gun/gun.obj', position=(.1, 0, .5), scale=0.1, parent=player)
crosshair = Entity(model='quad', texture='assets/gfx/crosshair.png', parent=camera.ui, scale=(.1, .1), position=(0, 0, 2), visible=True)
camera.rotation_x = 90
in_game = True
time_interval = 0.01
previous_position = player.position
# EditorCamera()
# ======= </Top Down Controller> ======

# ======= <Raycast Collision Handling and Gravity> =======
def move_with_raycast(direction):
    speed = 3 * time.dt
    ray = raycast(player.world_position, 
                  direction, 
                  ignore=(player,),
                  distance=0.5,
                  debug=True)

    if not ray.hit:
        player.position += direction * speed

gravity_force = 9.8
is_grounded = False
fall_speed = 0
max_fall_speed = 100

def apply_gravity():
    global fall_speed
    global is_grounded
    gravity_ray = raycast(player.world_position, 
                          Vec3(0, -1, 0), 
                          ignore=(player,),
                          distance=1/2,
                          debug=True)

    if not gravity_ray.hit:
        is_grounded = False
        fall_speed = min(fall_speed + gravity_force * time.dt, max_fall_speed)
        below_player_ray = raycast(player.world_position + Vec3(0, -0.5, 0), 
                                   Vec3(0, -1, 0), 
                                   ignore=(player,),
                                   distance=fall_speed * time.dt, 
                                   debug=True)

        if not below_player_ray.hit:
            player.y -= fall_speed * time.dt
    else:
        fall_speed = 0
        is_grounded = True

# ======= </Raycast Collision Handling and Gravity> ========

# ======= <MAP LAYOUT> =======
camera.shader = fxaa_shader
# camera.shader = ssao_shader
Sky()
Entity.default_shader = lit_with_shadows_shader
directional_light = DirectionalLight(shadow=True)
directional_light.look_at(Vec3(1, -1, -1))
the_giant_floor = Entity(model='cube', texture='brick', texture_scale=(50, 50), collider='box', scale=(50, .5, 50), position=(-1, -1, -1))
block = Entity(model='cube', collider='box', position=(3, 0, 0), color=color.red)
block2 = Entity(model='cube', collider='box', position=(-3, 0, 0), color=color.gray)
block3 = Entity(model='sphere', collider='sphere', position=(6, 0, 1), color=color.blue)
# ======= </MAP LAYOUT> ======

# ======= <HANDLING SHOOTING LOGIC> =======
bullets = []
def shoot():
    bullet = Entity(model='sphere', color=color.yellow, scale=0.2, position=equiped_gun.world_position, collider=None)
    bullet.direction = equiped_gun.forward
    bullet.speed = 300
    bullet.previous_position = bullet.position
    bullets.append(bullet)
# ======= </HANDLING SHOOTING LOGIC> =======

# ======= <UI> =======
# ---- <Start Screen> ----
controls_font = 'assets/fonts/Exo2-Regular.ttf'
title_controls = Text('Controls', color=color.white66, position=(-.47, .25), origin=(0, 0), scale=2, font='assets/fonts/zekton rg.otf')
frame = Entity(model='wireframe_cube', color=color.white33, position=(-.47, -.03), scale=(.4, .5), parent=camera.ui)
walk_controls = Text('W, A, S, D', position=(-.47, .1), origin=(0, 0), font=controls_font)
rightclick_control = Text('Right Click : Pickup/Throw weapons', position=(-.47, 0), origin=(0, 0), font=controls_font, scale=0.9)
leftclick_control = Text('Left Click : Shoot/Melee', position=(-.47, -.1), origin=(0, 0), font=controls_font)
# swipe_control = Text('Swipe Mouse : Curve bullets', position=(-.47, -.2), origin=(0, 0), font=controls_font)
controls_list = [title_controls, frame, walk_controls, rightclick_control, leftclick_control]
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
version = Text('Urisna TopDown Template V1.0', color=color.white, position=window.top_left, scale=1)
bg = Panel(origin=(0, 0), position=(0, 0), alpha=0.5, visible=False)
bg.scale_x = camera.aspect_ratio
bg.scale_y = camera.aspect_ratio
resume_text = Text('Press ESC again to resume', color=color.white, position=(0, 0.3), origin=(0, 0), scale=1.5, font='assets/fonts/zekton rg.otf', visible=False)
btn_options = Button(text='Options', origin=(0, 0), position=(0, -0.1), scale=(0.2, 0.05), disabled=True, visible=False, on_click=lambda: options() if not in_game else None)
btn_quit = Button(text='Quit', origin=(0, 0), position=(0, -0.2), scale=(0.2, 0.05), disabled=True, visible=False, on_click=lambda: application.quit if not in_game else None)
# ======= </UI> =======

# ======= <UPDATE AND INPUT FUNCTION FOR EVERYTHING> =======
def update():
    # ---- <Shooting> ----
    # <Gun>
    if in_game:
        for bullet in bullets:
            bullet.previous_position = bullet.position
            bullet.position += bullet.direction * bullet.speed * time.dt

            ray = raycast(bullet.previous_position, (bullet.position - bullet.previous_position).normalized(), ignore=(bullet,), distance=.3, debug=True)

            if ray.hit:
                destroy(bullet)
                bullets.remove(bullet)
                return

            if distance(player.position, bullet.position) > 40:
                destroy(bullet)
                bullets.remove(bullet)
    # </Gun>
    # ---- </Shooting> ----
    # ---- <Gravity> ----
    if in_game:
        apply_gravity()
    # ---- </Gravity> ----
    # ---- <Update Crosshair and Player Position/Roation> ----
    camera.position = lerp(camera.position, (player.x, player.y + 15, player.z), 10 * time.dt)
    crosshair.position = mouse.position
    if in_game:
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
    # ---- <Animation Handling> ----
    global previous_position
    global is_grounded

    if player.position != previous_position:
        player.model = sprint_animation
    else:  
        player.model = idle_animation
    
    invoke(lambda: store_position(), delay=time_interval)

    def store_position():
        global previous_position
        previous_position = player.position
    # ---- </Animation Handling > ----

def input(key):
    # ---- <Making variables global if needed, always do it here before anything> ----
    global in_game
    # ---- </Making variables global if needed, always do it here before anything> ----
    # ---- <Shooting> ----
    if in_game:
        if key == 'left mouse down':
            shoot()
    # ---- </Shooting> ----
    # ---- <Pause Menu> ----
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
            if 'in_options' in globals():
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

    # ---- <Old Animation handling method> ----
    # if in_game:
        # if held_keys['w']:
            # player.model = sprint_animation
        # elif held_keys['s']:
            # player.model = sprint_animation
        # elif held_keys['a']:
            # player.model = sprint_animation
        # elif held_keys['d']:
            # player.model = sprint_animation
        # else:
            # player.model = idle_animation
    # ---- </Old Animation handling method> ----
# ======= </UPDATE AND INPUT FUNCTION FOR EVERYTHING> ======
app.run()
