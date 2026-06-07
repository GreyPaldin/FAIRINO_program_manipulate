from fairino import Robot
import time
#Create
robot = Robot.RPC('192.168.159.128') #IP адрес виртуальной машины
if robot.RobotEnable(1) == 0:
    print("Robot activate")
if robot.Mode(0) == 0:
    print("Activate automal worked")
    
robot.ResetAllError()

error, joint_angles = robot.GetActualJointPosDegree(flag=1)

if error == 0:
    j1, j2, j3, j4, j5, j6 = joint_angles
    print(f"J1: {j1:.2f}°, J2: {j2:.2f}°, J3: {j3:.2f}°, J4: {j4:.2f}°, J5: {j5:.2f}°, J6: {j6:.2f}°")

def ArmHome(robot):
    home_pos = [0, -90, 90, 0, 90, 0]
    # Параметры:
    # joint_pos - целевые позиции суставов
    # tool - номер инструмента (обычно 0)
    # user - номер рабочего объекта (обычно 0)
    # vel - скорость в процентах (0-100)
    error = robot.MoveJ(home_pos, 0, 0, vel=100.0)
    print(error)

ArmHome(robot)
