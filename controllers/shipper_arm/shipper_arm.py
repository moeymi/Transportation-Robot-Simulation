from controller import Robot
import sys 

robot = Robot()

timestep = int(robot.getBasicTimeStep())

motors = []
gripper = []

for i in range(1,7):
    m = robot.getDevice("joint_" + str(i))
    m.setPosition(0)
    m.setVelocity(1.0)
    motors.append(m)
    
for i in range(1,3):
    g = robot.getDevice("joint_base_to_jaw_" + str(i))
    g.setPosition(0)
    g.setVelocity(1.0)
    gripper.append(g)

signal_receiver = robot.getDevice("signal_receiver")
signal_receiver.enable(timestep)

        
def step():
  if robot.step(timestep) == -1:
    exit(0)
  pass
  

def wait_until_seconds(secs):
  start_time = robot.getTime()
  while start_time + secs > robot.getTime():
    step()


def launch_load_unload():
    global motors, grippers
    
    motors[0].setVelocity(0.5)
    motors[1].setVelocity(0.5)
    motors[2].setVelocity(0.5)
    
    motors[0].setPosition(1.5)
    motors[1].setPosition(0.7)
    gripper[0].setPosition(0.01)
    gripper[1].setPosition(0.01)
    
    wait_until_seconds(3.5)
    motors[2].setPosition(0.5)
    
    wait_until_seconds(1.2)
    gripper[0].setPosition(0)
    gripper[1].setPosition(0)
    
    wait_until_seconds(1.5)
    motors[2].setPosition(0.3)
    
    wait_until_seconds(1.2)
    motors[0].setPosition(0)
    
    wait_until_seconds(3.0)
    motors[2].setPosition(0.5)
    
    wait_until_seconds(1.5)
    gripper[0].setPosition(0.01)
    gripper[1].setPosition(0.01)
    
    wait_until_seconds(0.3)
    motors[1].setPosition(0)
    motors[2].setPosition(0)


# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller

print(len(gripper))
while robot.step(timestep) != -1:

    load_sign = sys.argv[1]
    
    if (signal_receiver.getQueueLength() > 0):
      message = signal_receiver.getString()
      
      if (message == load_sign):
        launch_load_unload()
        
      signal_receiver.nextPacket()
      
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
