from fairino import Robot
import time

robot = Robot.RPC('192.168.159.128')

# Включение
robot.RobotEnable(1)
robot.Mode(1)  # ручной режим
robot.ResetAllError()

# Текущее положение
error, current = robot.GetActualJointPosDegree()
print(f"Было: J1 = {current[0]:.2f}°")

# Поворот на +90 градусов
target = current.copy()
target[0] = current[0] + 90
robot.MoveJ(target, 0, 0, vel=20.0)

# Ждем 5 секунд
time.sleep(5)

# Возврат
robot.MoveJ(current, 0, 0, vel=20.0)

print("Готово!")