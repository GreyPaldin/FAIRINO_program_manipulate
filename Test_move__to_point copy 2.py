from fairino import Robot
import time

robot = Robot.RPC('192.168.159.128')

# Подготовка
robot.RobotEnable(1)
robot.Mode(1)
robot.ResetAllError()
time.sleep(1)

# Текущая позиция: A (например, [300, 200, 400, 0, 0, 0])

# Промежуточная точка B
point_B = [-450.0, -300.0, 475.0, 90.0, 0.0, -90.0]

# Конечная точка C
point_C = [-600.0, -130.0, 475.0, 90.0, 0.0, -90.0]

# Движение по дуге A -> B -> C
error = robot.MoveC(point_B, 0, 0, point_C, 0, 0, vel_p=15.0, vel_t=15.0, blendR=-1.0)

if error == 0:
    print("✅ Движение по дуге запущено")
    
    # Ожидание завершения
    while True:
        err, done = robot.GetRobotMotionDone()
        if done == 1:
            break
        time.sleep(0.1)
    
    print("✅ Дуга завершена")
else:
    print(f"❌ Ошибка: {error}")