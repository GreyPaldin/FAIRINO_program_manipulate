from fairino import Robot
import time

robot = Robot.RPC('192.168.159.128')

# Подготовка
robot.RobotEnable(1)
robot.Mode(1)
robot.ResetAllError()
time.sleep(1)

# Базовое положение суставов (J1-J6 в градусах)
# Это положение: основание 0°, плечо -90°, локоть 90°, запястье 0°, 90°, 0°
home_joints = [0.0, -90.0, 90.0, 0.0, 90.0, 0.0]

print("Движение в базовое положение...")
error = robot.MoveJ(home_joints, 0, 0, vel=20.0, blendT=-1.0)

if error == 0:
    print("✅ Робот в базовом положении")
else:
    print(f"❌ Ошибка: {error}")