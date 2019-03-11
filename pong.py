# Implementation of classic arcade game Pong
# Run at http://www.codeskulptor.org/#user43_1jQqt59ygQ_14.py
import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

paddle1_pos = HEIGHT / 2   
paddle2_pos = HEIGHT / 2

paddle1_vel = 0
paddle2_vel = 0

ball_pos = [WIDTH/2, HEIGHT/2] # x,y
ball_vel = [0,1] 

countleft = 0
countright = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    # create random velocity at start of game to go upper right/left depending on who won 
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240) / 60
        ball_vel[1] = -random.randrange(60, 180) / 60
        ball_pos = [WIDTH/2, HEIGHT/2]
    else:
        ball_vel[0] = -random.randrange(120, 240) / 60
        ball_vel[1] = -random.randrange(60, 180) / 60
        ball_pos = [WIDTH/2, HEIGHT/2]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    spawn_ball(LEFT)       
    
def score(side):
    global countright, countleft
    # score counters
    if side == LEFT:
        countright += 1
    else:
        countleft += 1
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    # update ball position      
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # for increasing speed, below
    multiplier = 1.1
    
    # check to see if ball hit wall, then to see if it hit paddle, if it hit paddle,
    # bounce and increase speed of ball
    
    if ball_pos[0] <= BALL_RADIUS: #left wall (gutter)
        
        if paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
         
                ball_vel[0] = - ball_vel[0] * multiplier
        else:
                spawn_ball(RIGHT)
                score(RIGHT)
            
    elif ball_pos[0] >= WIDTH - BALL_RADIUS: #right wall (gutter)
        
        if paddle2_pos - HALF_PAD_HEIGHT  <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
        
            ball_vel[0] = -ball_vel[0] * multiplier
        else:
            spawn_ball(LEFT)
            score(LEFT)   
    
    # check to see if ball goes off the bottom/top
    if ball_pos[1] >= HEIGHT - BALL_RADIUS: # bottom canvas
        ball_vel[1] = -ball_vel[1]
    if ball_pos[1] <= BALL_RADIUS: # top canvas
        ball_vel[1] = -ball_vel[1]
        
        
#def dist(p, q):
    #return math.sqrt((ball_pos[0] - ball_pos2[0]) ** 2 + (ball_pos[1] - ball_pos2[1]) ** 2)
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
     
    # draw paddles
    paddle1 = canvas.draw_line( [HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "White")
    paddle2 = canvas.draw_line( [WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "White")
    
    
    # so you cant move the paddle off the screen
    
    if paddle1_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    elif paddle1_pos <  HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    if paddle2_pos < HALF_PAD_HEIGHT: # top right
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
        
    # update paddle    
        
    paddle1_pos = paddle1_pos + paddle1_vel
    paddle2_pos = paddle2_pos + paddle2_vel
    
    # draw scores on screen
    canvas.draw_text(str(countright), (265, 20), 22, 'White')
    canvas.draw_text(str(countleft), (320, 20), 22, 'White')
    
def keydown(key):
    global paddle1_vel, paddle2_vel, paddle1_pos, paddle2_pos
    
    if key == simplegui.KEY_MAP['w']:        
        paddle1_vel = paddle1_vel - 5    
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = paddle1_vel + 5        
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = paddle2_vel - 5    
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = paddle2_vel + 5
           
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0        
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0 

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
