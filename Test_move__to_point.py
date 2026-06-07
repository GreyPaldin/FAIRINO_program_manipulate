from fairino import Robot
import time
import sys

robot = Robot.RPC('192.168.55.128')

def prepare_robot():
    """Подготовка робота (без загрузки программы)"""
    print("\n" + "=" * 60)
    print("ПОДГОТОВКА РОБОТА")
    print("=" * 60)
    
    robot.RobotEnable(1)
    robot.Mode(1)
    robot.ResetAllError()
    time.sleep(1)
    
    error, state = robot.GetSDKComState()
    if error == 0 and state == 0:
        print("✅ Робот готов")
        return True
    print("❌ Ошибка подключения")
    return False

def move_to_point(point, speed=15.0):
    """Движение к точке"""
    print(f"\n📍 Точка: X={point[0]:.1f}, Y={point[1]:.1f}, Z={point[2]:.1f}")
    
    error = robot.MoveL(point, 0, 0, vel=speed, blendR=-1.0)
    
    if error != 0:
        print(f"   ❌ Ошибка MoveL: {error}")
        return False
    
    print("   ⏳ Движение...", end="", flush=True)
    while True:
        err, done = robot.GetRobotMotionDone()
        if done == 1:
            break
        time.sleep(0.1)
    print(" ✅")
    return True

# ============================================
# ОСНОВНАЯ ПРОГРАММА
# ============================================

if __name__ == "__main__":
    if not prepare_robot():
        sys.exit(1)
    
    points = [
        [-497.0, -130.0, 476.0, -180.0, 0.0, 180.0],
        [-500.0, -200.0, 200.0, -180.0, 0.0, 180.0],
        [-400.0, -200.0, 200.0, -180.0, 0.0, 180.0],
        [-400.0, -200.0, 300.0, -180.0, 0.0, 180.0],
        [-500.0, -200.0, 300.0, -180.0, 0.0, 180.0],
        [-497.0, -130.0, 476.0, -180.0, 0.0, 180.0],
    ]
    
    print("\n" + "=" * 60)
    print("ДВИЖЕНИЕ ПО ТОЧКАМ")
    print("=" * 60)
    
    confirm = input("\nНачать движение? (Y/Yes/Д/Да): ").strip().lower()
    if confirm not in ['y', 'yes', 'д', 'да']:
        print("❌ Движение отменено")
        sys.exit(0)
    
    for i, point in enumerate(points):
        print(f"\n--- Точка {i+1} из {len(points)} ---")
        move_to_point(point, speed=15.0)
    
    print("\n✅ Программа завершена")