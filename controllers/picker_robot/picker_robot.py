"""picker_robot controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Camera

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = 32

# Create a camera object
camera = None

right_motor = robot.getDevice("front_right_motor")
right_motor.setPosition(float('inf'))
right_motor.setVelocity(0)

left_motor = robot.getDevice("front_left_motor")
left_motor.setPosition(float('inf'))
left_motor.setVelocity(0)


right2_motor = robot.getDevice("back_right_motor")
right2_motor.setPosition(float('inf'))
right2_motor.setVelocity(0)

left2_motor = robot.getDevice("back_left_motor")
left2_motor.setPosition(float('inf'))
left2_motor.setVelocity(0)


# Set the camera's width and height
#camera.enable(timestep)

#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

max_speed = 7

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:

    vel = max_speed * 0.5
    right_motor.setVelocity(vel)
    left_motor.setVelocity(vel)
    right2_motor.setVelocity(vel)
    left2_motor.setVelocity(vel)

    if camera is None:
        continue
    image = camera.getImageArray()
    if image:
        red   = image[0][0][0]
        green = image[0][0][1]
        blue  = image[0][0][2]
        gray  = (red + green + blue) / 3
        print('r='+str(red)+' g='+str(green)+' b='+str(blue))

    pass

# Enter here exit cleanup code.
