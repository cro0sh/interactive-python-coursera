# Spaceship
# Interactive Programming w/ Python Part 2
# Run at http://www.codeskulptor.org/#user43_kgjq3vUOI6_11.py
# Beta 

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
accel_multiplier = 1.2
friction_constant = .05     
angle_ship = .0475
orientation = {"left": -angle_ship, "right": angle_ship}
left_or_right = 0
angle_missle = 45
missle_vel_percentage = .25
missle = False 

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_info_t = ImageInfo([135, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
ship_thrust_sound.set_volume(.5)
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):    
    return [math.cos(ang), math.sin(ang)]
    

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        if sound:
            sound.rewind()
            sound.play()
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        if self.thrust:
            self.vel[0] += angle_to_vector(self.angle)[0] * accel_multiplier
            self.vel[1] += angle_to_vector(self.angle)[1] * accel_multiplier            
        
        self.vel[0] *= (1-friction_constant)
        self.vel[1] *= (1-friction_constant)
        
        if self.pos[1] >= HEIGHT - self.radius:
            self.pos[1] = self.radius   
                        
        if self.pos[1] < self.radius:
            self.pos[1] = HEIGHT - self.radius      
                        
        if self.pos[0] <= self.radius:
            self.pos[0] = WIDTH - self.radius
            
        if self.pos[0] > WIDTH - self.radius:
            self.pos[0] = self.radius       
             
                 
    def shoot(self):
        global a_missle_two
        
        a_missle_two = Sprite([self.pos[0], self.pos[1]], [self.vel[0],self.vel[0]], self.angle, self.angle_vel, missile_image, missile_info, missile_sound)
       
        x = angle_to_vector(self.angle)[0] * angle_missle
        y = angle_to_vector(self.angle)[1] * angle_missle     
        
        a_missle_two.pos[0] = my_ship.pos[0] + x
        a_missle_two.pos[1] = my_ship.pos[1] + y
        
        a_missle_two.vel[0] += self.vel[0] + x * missle_vel_percentage
        a_missle_two.vel[1] += self.vel[1] + y * missle_vel_percentage
        
        return a_missle_two
            
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.thrust = False
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        
        if self.pos[1] >= HEIGHT - self.radius:
            self.pos[1] = self.radius   
                        
        if self.pos[1] < self.radius:
            self.pos[1] = HEIGHT - self.radius      
                        
        if self.pos[0] <= self.radius:
            self.pos[0] = WIDTH - self.radius
            
        if self.pos[0] > WIDTH - self.radius:
            self.pos[0] = self.radius    
    
    def random_number(self):
        randnum = [random.randint(0,WIDTH), random.randint(0,HEIGHT)]
        return randnum
    
    def random_float(self, a, b):
        increment = .002
        i = a
        lst = []
        while i < b:        
            i += increment
            lst.append(i)
        return random.choice(lst)
            
def keyup(key):
    global left_or_right
    
    if key == simplegui.KEY_MAP['down']:      
        left_or_right = 0        
               
    if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
        left_or_right = 0
        
    if key == simplegui.KEY_MAP['up']:        
        my_ship.thrust = False        
        my_ship_thrust.thrust = False
        
        my_ship.vel[0] = my_ship_thrust.vel[0]
        my_ship.vel[1] = my_ship_thrust.vel[1]


def keydown(key):
    global left_or_right, missle
    
    for keys, values in orientation.items():
        if key == simplegui.KEY_MAP[keys]:
            left_or_right = values    
            

            if key == simplegui.KEY_MAP['up']:
                my_ship.thrust = True
                my_ship_thrust.thrust = True                   
    
        if key == simplegui.KEY_MAP['up']:
            my_ship.thrust = True 
            my_ship_thrust.thrust = True 
                     
            
        if key == simplegui.KEY_MAP['space']:
            my_ship.shoot()
            my_ship_thrust.shoot()
            missle = True            
            
def draw(canvas):
    global time
    
    # so angle of ship continues to turn on hold down of key
    my_ship.angle += left_or_right
    my_ship_thrust.angle += left_or_right    

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # display lives and scores
    canvas.draw_text(str(lives) + ' lives', (50, 50), 40, 'White')
    canvas.draw_text('score: ' + str(score), (625, 50), 40, 'White')
    
    # logic for drawing thrust image or not    
    if my_ship_thrust.thrust:
        my_ship_thrust.draw(canvas)
        ship_thrust_sound.play()
        
    else:
        my_ship.draw(canvas)       	
        ship_thrust_sound.pause()   
        
    # draw ship and sprites    
    a_rock.draw(canvas) 
    
    if missle:
        a_missle_two.draw(canvas)
        a_missle_two.update()
    
    # update ship and sprites
    my_ship.update()
    my_ship_thrust.update()
    a_rock.update()
    my_ship_t.update()
   

            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    a_rock = Sprite([a_rock.random_number()[0], a_rock.random_number()[1]], [a_rock.random_float(-.2,.5), a_rock.random_float(-.3,.6)], 0, a_rock.random_float(-.1,.1), asteroid_image, asteroid_info)
    

#(self, pos, vel, ang, ang_vel, image, info, sound = None):
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
a_missle_two =  Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
       
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [0.3, 0.4], 0, 0.1, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
my_ship_thrust = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info_t, ship_thrust_sound)
my_ship_t = Sprite([WIDTH / 2, HEIGHT / 2], [0, 0], 0, 0, ship_image, ship_info_t, ship_thrust_sound)
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
