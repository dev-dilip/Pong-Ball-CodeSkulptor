# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 800
HEIGHT = 600       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new ball in middle of table
ball_pos = [WIDTH/2,HEIGHT/2]
ball_vel = [0,0]
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0


# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global  ball_vel # these are vectors stored as lists
    if direction is RIGHT:
        ball_vel[0] = random.randrange(5,10)

    if direction is LEFT:
        ball_vel[0] = -random.randrange(5,10)

        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global ball_pos, ball_vel
    #ball_pos = [WIDTH/2,HEIGHT/2]
    ball_vel = [0,3]
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2,"White", "White")
    
    # draw paddles
    canvas.draw_line((0,paddle1_pos - HALF_PAD_HEIGHT),(0,paddle1_pos + HALF_PAD_HEIGHT), 16, "White")
    canvas.draw_line((WIDTH,paddle2_pos - HALF_PAD_HEIGHT),(WIDTH,paddle2_pos + HALF_PAD_HEIGHT), 16, "White")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    paddle2_pos += paddle2_vel
    
    # determine whether paddle and ball collide 
    if paddle1_pos <= HALF_PAD_HEIGHT:		
        paddle1_pos = HALF_PAD_HEIGHT
        
    if paddle1_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
            
    if paddle2_pos <= HALF_PAD_HEIGHT:		
        paddle2_pos = HALF_PAD_HEIGHT
        
    if paddle2_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
    
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # draw scores
    canvas.draw_text(str(score1), (WIDTH*0.25, 40), 40, 'White')
    canvas.draw_text(str(score2), (WIDTH*0.75, 40), 40, 'White')    
    
    if ball_pos[0] <= BALL_RADIUS+PAD_WIDTH:
        if ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            if ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT:
                ball_pos[0] = BALL_RADIUS + PAD_WIDTH
                ball_vel[0] = -ball_vel[0]*1.1
            else:
                score2 += 1
                spawn_ball(RIGHT)
        else:
            score2 += 1
            spawn_ball(RIGHT)

    if ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:	
        if ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            if ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT:
                ball_pos[0] = WIDTH - PAD_WIDTH - BALL_RADIUS
                ball_vel[0] = -ball_vel[0]*1.1
            else:
                score1 += 1
                spawn_ball(LEFT)      
        else:
            score1 += 1
            spawn_ball(LEFT)
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel += 4
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel -= 4  
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel += 4
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel -= 4 
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel -= 4
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel += 4
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel -= 4
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel += 4 
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
canvas = frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

button = frame.add_button("New Game", new_game, 100)

# start frame
frame.start()