from controller import Robot, Camera

from webcolors import rgb_to_name
import time

robot = Robot()

timestep = int(robot.getBasicTimeStep())

max_speed = 8

color_camera = Camera('color_camera')

left_ds = robot.getDevice("left_ds")
right_ds = robot.getDevice("right_ds")

left_ds.enable(timestep)
right_ds.enable(timestep)

right_motor = robot.getDevice("right_motor")
left_motor = robot.getDevice("left_motor")

left_led = robot.getDevice("left_led")
right_led = robot.getDevice("right_led")

right_motor.setPosition(float('inf'))
right_motor.setVelocity(0)

left_motor.setPosition(float('inf'))
left_motor.setVelocity(0)

ds = robot.getDevice("distance_sensor")
ds.enable(timestep)

emitter = robot.getDevice("signal_emitter")

prev_state = current_state = 'free'

time_counter = (0, 0)

current_load = 1

def round_color(value):
    if value < 128:
        return 0
    else:
        return 255


def set_velocities(velocities):
    left_motor.setVelocity(velocities[0])
    right_motor.setVelocity(velocities[1])
    
    
def move_straight():
    right_led.set(1)
    left_led.set(1)
    set_velocities((max_speed, max_speed))
    
    
def rotate_left():
    right_led.set(1)
    left_led.set(2)
    set_velocities((0, max_speed / 2))
    
    
def rotate_right():
    right_led.set(2)
    left_led.set(1)
    set_velocities((max_speed / 2, 0))


def stop():
    set_velocities((0, 0))

def get_color_beneath(camera):
    if camera is not None:
        image = camera.getImageArray()
        if image:
            red   = image[0][0][0]
            green = image[0][0][1]
            blue  = image[0][0][2]
            
            red = round_color(red)
            green = round_color(green)
            blue = round_color(blue)
            return rgb_to_name((red, green, blue))
            
            
def follow_line():
    left_color = left_ds.getValue()
    right_color = right_ds.getValue()
    
    if abs(left_color - right_color) < 100:
        move_straight()
        
    elif left_color > 400 :
        rotate_left()
        
    elif right_color > 400:
        rotate_right()


def decide_on_state(prevstate, state):
    color = get_color_beneath(color_camera)
    global current_load
    if prevstate != state:
        if prevstate == 'free':
            emitter.send(str(current_load) + "l")
        elif prevstate == 'loaded':
            emitter.send(str(current_load) + "u")
            
    if state == 'waiting_load' or state == 'waiting_unload':
        stop()
    else:
        follow_line()


def decide_state(state):
    global time_counter, current_load
    
    color = get_color_beneath(color_camera)
    if color == 'red':
        return 'finished'
    
    if color == 'magenta' and state == 'free':
        return 'waiting_load'
    if color == 'blue' and state == 'loaded':
        return 'waiting_unload'
    
    load_dist = ds.getValue()
    
    if state == 'waiting_load' and load_dist < 500:
        time_counter = (robot.getTime(), 3)
        return 'loaded'
         
    if state == 'waiting_unload' and load_dist > 500:
        time_counter = (robot.getTime(), 3)
        current_load+=1
        return 'free'
        
    return state

def wait_for_timer():
    global time_counter
    if time_counter[1] > 0:
        if robot.getTime() - time_counter[0] <= time_counter[1]:
            return True
        else:
            time_counter = (0, 0)
            
    return False

while robot.step(timestep) != -1:
    if current_state == 'finished':
        stop()
        break
    
    if wait_for_timer():
        continue
        
    decide_on_state(prev_state, current_state)
    
    prev_state = current_state
    current_state = decide_state(current_state)
    pass
    

# Enter here exit cleanup code.
