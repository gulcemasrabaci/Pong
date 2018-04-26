import simplegui
import random

WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
PAD_VEL = 4

def spawn_ball(direction):
    """initializes ball_pos and ball_vel"""
    global ball_pos, ball_vel    
    
    ball_vel = [0, 0]
    ball_pos = [WIDTH / 2, HEIGHT / 2]
   
    x_per_sec = random.randrange(120, 240)
    y_per_sec = -random.randrange(60, 180)
    #these per second velocity values will be divided by 60 to calculate the
    #ball_vel components, since the draw handler is called 60 times per second
        
    if direction == RIGHT:
        ball_vel[0] = x_per_sec / 60.0    
    else:
        ball_vel[0] = (-x_per_sec) / 60.0
    ball_vel[1] = y_per_sec / 60.0
    
# define event handlers
def new_game():
    """resets score, calls spawn_ball"""
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    
    paddle1_pos = HALF_PAD_HEIGHT
    paddle2_pos = HALF_PAD_HEIGHT
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    
    balldir = random.randrange(0,2)
    if balldir == 0:
        spawn_ball(LEFT)
    else:
        spawn_ball(RIGHT)
      
def draw(canvas):
    """draws field, ball, paddles, scores."""
    """handles collision with gutters and paddles"""
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
         
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
         
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if HALF_PAD_HEIGHT <= paddle1_pos + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    
    if HALF_PAD_HEIGHT <= paddle2_pos + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel  

    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], 
                         [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], [0, paddle1_pos + HALF_PAD_HEIGHT]],
                        2, "Red", "Red")
   
    canvas.draw_polygon([[WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], 
                         [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH, paddle2_pos + HALF_PAD_HEIGHT]],
                        2, "Red", "Red")    
    
    # determine whether paddle and ball collide    
    if ball_pos[1] + ball_vel[1] - BALL_RADIUS <= 0 or ball_pos[1] + ball_vel[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] *= -1    
    
    elif ball_pos[0] + ball_vel[0] - BALL_RADIUS <= PAD_WIDTH:
        if paddle1_pos - HALF_PAD_HEIGHT > ball_pos[1] + ball_vel[1] + BALL_RADIUS or paddle1_pos + HALF_PAD_HEIGHT < ball_pos[1] + ball_vel[1] - BALL_RADIUS:
            score2 += 1
            spawn_ball(RIGHT)
        else:
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
            
    elif ball_pos[0] + ball_vel[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        if paddle2_pos - HALF_PAD_HEIGHT > ball_pos[1] + ball_vel[1] + BALL_RADIUS or paddle2_pos + HALF_PAD_HEIGHT < ball_pos[1] + ball_vel[1] - BALL_RADIUS:
            score1 += 1
            spawn_ball(LEFT)
        else:
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1

    # draw scores 
    canvas.draw_text(str(score1), [150, 80], 50, "White")
    canvas.draw_text(str(score2), [430, 80], 50, "White")
        
def keydown(key):
    """moves paddles according to keyboard input"""
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -PAD_VEL
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -PAD_VEL
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = PAD_VEL
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = PAD_VEL
   
def keyup(key):
    """stops paddle movement according to keyboard input"""
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw) #draw handler runs 60 times a second
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)

new_game()
frame.start()