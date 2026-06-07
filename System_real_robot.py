from fairino import Robot
import time
import sys

# ============================================
# ГЛОБАЛЬНЫЕ НАСТРОЙКИ
# ============================================

# ПОДКЛЮЧЕНИЕ К РОБОТУ
ROBOT_IP = "192.168.55.129"

# Включение/выключение проверки рабочей зоны
WORKSPACE_CHECK_ENABLED = False

# Ограничения рабочей зоны (прямоугольный параллелепипед)
# X, Y, Z в миллиметрах
WORKSPACE_LIMITS = {
    'x_min': -500.0,
    'x_max': 800.0,
    'y_min': -500.0,
    'y_max': 500.0,
    'z_min': 0.0,
    'z_max': 900.0
}

# Глобальные переменные для текущих базисов (используются в движении)
CURRENT_TOOL = 0
CURRENT_WOBJ = 0

print("Подключение к " + ROBOT_IP + "...")
# SDK: Создание RPC-клиента для подключения к контроллеру робота
robot = Robot.RPC(ROBOT_IP)
time.sleep(1)

# ПРОВЕРКА СВЯЗИ
try:
    # SDK: GetSDKComState - проверка состояния связи с контроллером
    result = robot.GetSDKComState()
    if isinstance(result, tuple):
        error, state = result
        if error == 0 and state == 0:
            print("Связь установлена")
        else:
            print("Ошибка связи: error=" + str(error) + ", state=" + str(state))
            sys.exit(1)
    else:
        if result == 0:
            print("Связь установлена")
        else:
            print("Ошибка связи: " + str(result))
            sys.exit(1)
except Exception as e:
    print("Ошибка при проверке связи: " + str(e))
    sys.exit(1)

# ============================================
# ФУНКЦИИ РАБОТЫ С БАЗИСАМИ
# ============================================

def show_current_bases():
    """Показать текущие номера инструмента и системы координат"""
    print("\n" + "=" * 60)
    print("ТЕКУЩИЕ БАЗИСЫ")
    print("=" * 60)
    
    # SDK: GetActualTCPNum - получение текущего номера инструмента
    error, tool_num = robot.GetActualTCPNum()
    if error == 0:
        print("\n  Текущий инструмент (tool): " + str(tool_num))
        if tool_num == 0:
            print("    (базовый инструмент, без смещения)")
        else:
            # SDK: GetToolCoordWithID - получение смещения инструмента по его номеру
            error, coord = robot.GetToolCoordWithID(tool_num)
            if error == 0:
                print("    Смещение: X=" + format(coord[0], ".1f") + 
                      " Y=" + format(coord[1], ".1f") + 
                      " Z=" + format(coord[2], ".1f"))
    else:
        print("  Ошибка получения инструмента: " + str(error))
    
    # SDK: GetActualWObjNum - получение текущего номера системы координат объекта
    error, wobj_num = robot.GetActualWObjNum()
    if error == 0:
        print("\n  Текущий объект (user): " + str(wobj_num))
        if wobj_num == 0:
            print("    (мировая система координат)")
        else:
            # SDK: GetWObjCoordWithID - получение смещения системы координат объекта по номеру
            error, coord = robot.GetWObjCoordWithID(wobj_num)
            if error == 0:
                print("    Смещение: X=" + format(coord[0], ".1f") + 
                      " Y=" + format(coord[1], ".1f") + 
                      " Z=" + format(coord[2], ".1f"))
    else:
        print("  Ошибка получения объекта: " + str(error))
    
    print("\n  Используемые в движении:")
    print("    CURRENT_TOOL = " + str(CURRENT_TOOL))
    print("    CURRENT_WOBJ = " + str(CURRENT_WOBJ))
    
    print("\n" + "=" * 60)


def select_current_tool():
    """Выбрать текущий инструмент для движения (без редактирования)"""
    global CURRENT_TOOL
    print("\n" + "=" * 60)
    print("ВЫБОР ТЕКУЩЕГО ИНСТРУМЕНТА")
    print("=" * 60)
    
    # SDK: GetActualTCPNum - получение текущего номера инструмента
    error, current = robot.GetActualTCPNum()
    if error == 0:
        print("\nТекущий инструмент в контроллере: " + str(current))
    
    print("\nДоступные инструменты:")
    print("  0 - Базовый инструмент (фланец, без смещения)")
    print("  1-14 - Пользовательские инструменты (настроенные ранее)")
    
    while True:
        try:
            tool_num = int(input("\nВведите номер инструмента (0-14): "))
            if 0 <= tool_num <= 14:
                break
            print("Ошибка: введите число от 0 до 14")
        except ValueError:
            print("Ошибка: введите число")
    
    CURRENT_TOOL = tool_num
    print("\nИнструмент для движения установлен: " + str(CURRENT_TOOL))
    
    # Показываем смещение выбранного инструмента
    if tool_num == 0:
        print("  (базовый инструмент, без смещения)")
    else:
        error, coord = robot.GetToolCoordWithID(tool_num)
        if error == 0:
            print("  Смещение: X=" + format(coord[0], ".1f") + 
                  " Y=" + format(coord[1], ".1f") + 
                  " Z=" + format(coord[2], ".1f"))
    
    print("=" * 60)


def select_current_wobj():
    """Выбрать текущую систему координат объекта для движения (без редактирования)"""
    global CURRENT_WOBJ
    print("\n" + "=" * 60)
    print("ВЫБОР ТЕКУЩЕЙ СИСТЕМЫ КООРДИНАТ ОБЪЕКТА")
    print("=" * 60)
    
    # SDK: GetActualWObjNum - получение текущего номера объекта
    error, current = robot.GetActualWObjNum()
    if error == 0:
        print("\nТекущий объект в контроллере: " + str(current))
    
    print("\nДоступные объекты:")
    print("  0 - Мировая система координат")
    print("  1-14 - Пользовательские системы координат (настроенные ранее)")
    
    while True:
        try:
            wobj_num = int(input("\nВведите номер объекта (0-14): "))
            if 0 <= wobj_num <= 14:
                break
            print("Ошибка: введите число от 0 до 14")
        except ValueError:
            print("Ошибка: введите число")
    
    CURRENT_WOBJ = wobj_num
    print("\nСистема координат для движения установлена: " + str(CURRENT_WOBJ))
    
    # Показываем смещение выбранного объекта
    if wobj_num == 0:
        print("  (мировая система координат)")
    else:
        error, coord = robot.GetWObjCoordWithID(wobj_num)
        if error == 0:
            print("  Смещение: X=" + format(coord[0], ".1f") + 
                  " Y=" + format(coord[1], ".1f") + 
                  " Z=" + format(coord[2], ".1f"))
    
    print("=" * 60)


def show_all_tools():
    """Показать все настроенные инструменты (1-14)"""
    print("\n" + "=" * 60)
    print("СПИСОК НАСТРОЕННЫХ ИНСТРУМЕНТОВ")
    print("=" * 60)
    
    found = False
    for i in range(1, 15):
        error, coord = robot.GetToolCoordWithID(i)
        if error == 0:
            if coord[0] != 0 or coord[1] != 0 or coord[2] != 0 or coord[3] != 0 or coord[4] != 0 or coord[5] != 0:
                print("\nИнструмент " + str(i) + ":")
                print("  Смещение (мм): X=" + format(coord[0], ".1f") + 
                      "  Y=" + format(coord[1], ".1f") + 
                      "  Z=" + format(coord[2], ".1f"))
                print("  Ориентация (град): Rx=" + format(coord[3], ".1f") + 
                      "  Ry=" + format(coord[4], ".1f") + 
                      "  Rz=" + format(coord[5], ".1f"))
                found = True
    
    if not found:
        print("\nНет настроенных инструментов (все нулевые)")
    print("\n" + "=" * 60)


def show_all_wobjs():
    """Показать все настроенные системы координат (1-14)"""
    print("\n" + "=" * 60)
    print("СПИСОК НАСТРОЕННЫХ СИСТЕМ КООРДИНАТ")
    print("=" * 60)
    
    found = False
    for i in range(1, 15):
        # SDK: GetWObjCoordWithID - получение смещения системы координат объекта по номеру
        error, coord = robot.GetWObjCoordWithID(i)
        if error == 0:
            if coord[0] != 0 or coord[1] != 0 or coord[2] != 0 or coord[3] != 0 or coord[4] != 0 or coord[5] != 0:
                print("\nОбъект " + str(i) + ":")
                print("  Позиция (мм): X=" + format(coord[0], ".1f") + 
                      "  Y=" + format(coord[1], ".1f") + 
                      "  Z=" + format(coord[2], ".1f"))
                print("  Ориентация (град): Rx=" + format(coord[3], ".1f") + 
                      "  Ry=" + format(coord[4], ".1f") + 
                      "  Rz=" + format(coord[5], ".1f"))
                found = True
    
    if not found:
        print("\nНет настроенных систем координат (все нулевые)")
    print("\n" + "=" * 60)


def configure_tool():
    """Настроить инструмент (задать смещение) - ТОЛЬКО 1-14"""
    print("\n" + "=" * 60)
    print("НАСТРОЙКА ИНСТРУМЕНТА")
    print("=" * 60)
    print("Примечание: инструмент 0 (базовый) нельзя настроить")
    
    while True:
        try:
            tool_num = int(input("Введите номер инструмента (1-14): "))
            if 1 <= tool_num <= 14:
                break
            print("Ошибка: введите число от 1 до 14")
        except ValueError:
            print("Ошибка: введите число")
    
    print("\nВведите смещение относительно фланца:")
    try:
        x = float(input("X (мм, Enter=0): ") or "0")
        y = float(input("Y (мм, Enter=0): ") or "0")
        z = float(input("Z (мм, Enter=0): ") or "0")
        rx = float(input("Rx (град, Enter=0): ") or "0")
        ry = float(input("Ry (град, Enter=0): ") or "0")
        rz = float(input("Rz (град, Enter=0): ") or "0")
    except ValueError:
        print("Ошибка ввода")
        return
    
    coord = [x, y, z, rx, ry, rz]
    # SDK: SetToolCoord - установка параметров инструмента (номер, смещение, тип, установка, ID, нагрузка)
    error = robot.SetToolCoord(tool_num, coord, 0, 0, 0, 0)
    if error == 0:
        print("Инструмент " + str(tool_num) + " настроен")
    else:
        print("Ошибка: " + str(error))


def configure_wobj():
    """Настроить систему координат объекта - ТОЛЬКО 1-14"""
    print("\n" + "=" * 60)
    print("НАСТРОЙКА СИСТЕМЫ КООРДИНАТ ОБЪЕКТА")
    print("=" * 60)
    print("Примечание: объект 0 (мировой) нельзя настроить")
    
    while True:
        try:
            wobj_num = int(input("Введите номер объекта (1-14): "))
            if 1 <= wobj_num <= 14:
                break
            print("Ошибка: введите число от 1 до 14")
        except ValueError:
            print("Ошибка: введите число")
    
    print("\nВведите смещение относительно мировой системы:")
    try:
        x = float(input("X (мм, Enter=0): ") or "0")
        y = float(input("Y (мм, Enter=0): ") or "0")
        z = float(input("Z (мм, Enter=0): ") or "0")
        rx = float(input("Rx (град, Enter=0): ") or "0")
        ry = float(input("Ry (град, Enter=0): ") or "0")
        rz = float(input("Rz (град, Enter=0): ") or "0")
    except ValueError:
        print("Ошибка ввода")
        return
    
    coord = [x, y, z, rx, ry, rz]
    # SDK: SetWObjCoord - установка системы координат объекта
    error = robot.SetWObjCoord(wobj_num, coord, 0)
    if error == 0:
        print("Объект " + str(wobj_num) + " настроен")
    else:
        print("Ошибка: " + str(error))


def reset_tool():
    """Сбросить инструмент в ноль - ТОЛЬКО 1-14"""
    print("\n" + "=" * 60)
    print("СБРОС ИНСТРУМЕНТА")
    print("=" * 60)
    print("Примечание: инструмент 0 (базовый) нельзя сбросить, он всегда нулевой")
    
    while True:
        try:
            tool_num = int(input("Введите номер инструмента для сброса (1-14): "))
            if 1 <= tool_num <= 14:
                break
            print("Ошибка: введите число от 1 до 14")
        except ValueError:
            print("Ошибка: введите число")
    
    coord = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # SDK: SetToolCoord - установка нулевого смещения для инструмента
    error = robot.SetToolCoord(tool_num, coord, 0, 0, 0, 0)
    if error == 0:
        print("Инструмент " + str(tool_num) + " сброшен в ноль")
    else:
        print("Ошибка: " + str(error))


def reset_wobj():
    """Сбросить систему координат объекта в ноль - ТОЛЬКО 1-14"""
    print("\n" + "=" * 60)
    print("СБРОС СИСТЕМЫ КООРДИНАТ ОБЪЕКТА")
    print("=" * 60)
    print("Примечание: объект 0 (мировой) нельзя сбросить, он всегда нулевой")
    
    while True:
        try:
            wobj_num = int(input("Введите номер объекта для сброса (1-14): "))
            if 1 <= wobj_num <= 14:
                break
            print("Ошибка: введите число от 1 до 14")
        except ValueError:
            print("Ошибка: введите число")
    
    coord = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # SDK: SetWObjCoord - установка нулевого смещения для системы координат объекта
    error = robot.SetWObjCoord(wobj_num, coord, 0)
    if error == 0:
        print("Объект " + str(wobj_num) + " сброшен в ноль")
    else:
        print("Ошибка: " + str(error))

# ============================================
# ФУНКЦИЯ ПРОВЕРКИ ДОСТИЖИМОСТИ
# ============================================

def is_point_reachable(point):
    """Проверка достижимости точки через обратную кинематику"""
    try:
        # SDK: GetActualJointPosDegree - получение текущих углов суставов
        error, current_joints = robot.GetActualJointPosDegree()
        if error != 0:
            print("   Не удалось получить текущие углы")
            return False
        
        # SDK: GetInverseKinHasSolution - проверка наличия решения обратной кинематики
        error, result = robot.GetInverseKinHasSolution(0, point, current_joints)
        return (error == 0 and result == True)
    except Exception as e:
        print("   Ошибка проверки: " + str(e))
        return False


def is_point_in_workspace(point):
    """Проверка нахождения точки в рабочей зоне (по X, Y, Z)"""
    if not WORKSPACE_CHECK_ENABLED:
        return True
    
    x, y, z = point[0], point[1], point[2]
    
    if x < WORKSPACE_LIMITS['x_min'] or x > WORKSPACE_LIMITS['x_max']:
        print("   Точка вне зоны: X=" + format(x, ".1f") + " (допустимо " + 
              format(WORKSPACE_LIMITS['x_min'], ".0f") + "..." + 
              format(WORKSPACE_LIMITS['x_max'], ".0f") + ")")
        return False
    
    if y < WORKSPACE_LIMITS['y_min'] or y > WORKSPACE_LIMITS['y_max']:
        print("   Точка вне зоны: Y=" + format(y, ".1f") + " (допустимо " + 
              format(WORKSPACE_LIMITS['y_min'], ".0f") + "..." + 
              format(WORKSPACE_LIMITS['y_max'], ".0f") + ")")
        return False
    
    if z < WORKSPACE_LIMITS['z_min'] or z > WORKSPACE_LIMITS['z_max']:
        print("   Точка вне зоны: Z=" + format(z, ".1f") + " (допустимо " + 
              format(WORKSPACE_LIMITS['z_min'], ".0f") + "..." + 
              format(WORKSPACE_LIMITS['z_max'], ".0f") + ")")
        return False
    
    return True


def check_point_safe(point):
    """Полная проверка точки (достижимость + рабочая зона)"""
    if not is_point_in_workspace(point):
        return False
    
    if not is_point_reachable(point):
        print("   Точка недостижима (нет решения обратной кинематики)")
        return False
    
    return True


def get_current_tcp():
    """Получить текущую TCP позицию"""
    try:
        # SDK: GetActualTCPPose - получение текущей позиции инструмента в пространстве
        error, tcp = robot.GetActualTCPPose()
        if error == 0:
            return tcp
        else:
            print("Ошибка получения TCP: " + str(error))
            return None
    except Exception as e:
        print("Ошибка: " + str(e))
        return None


# ============================================
# ФУНКЦИИ УПРАВЛЕНИЯ РАБОЧЕЙ ЗОНОЙ
# ============================================

def show_workspace_limits():
    """Показать текущие ограничения рабочей зоны"""
    print("\n" + "=" * 60)
    print("ОГРАНИЧЕНИЯ РАБОЧЕЙ ЗОНЫ")
    print("=" * 60)
    
    status = "ВКЛЮЧЕНА" if WORKSPACE_CHECK_ENABLED else "ВЫКЛЮЧЕНА"
    print("\nСтатус проверки зоны: " + status)
    
    if WORKSPACE_CHECK_ENABLED:
        print("\nДопустимые пределы (X, Y, Z в мм):")
        print("  X: от " + format(WORKSPACE_LIMITS['x_min'], ".0f") + " до " + format(WORKSPACE_LIMITS['x_max'], ".0f"))
        print("  Y: от " + format(WORKSPACE_LIMITS['y_min'], ".0f") + " до " + format(WORKSPACE_LIMITS['y_max'], ".0f"))
        print("  Z: от " + format(WORKSPACE_LIMITS['z_min'], ".0f") + " до " + format(WORKSPACE_LIMITS['z_max'], ".0f"))
        
        current = get_current_tcp()
        if current is not None:
            print("\nТекущая позиция инструмента:")
            print("  X=" + format(current[0], ".1f") + "  Y=" + format(current[1], ".1f") + "  Z=" + format(current[2], ".1f"))
            
            if (current[0] < WORKSPACE_LIMITS['x_min'] or current[0] > WORKSPACE_LIMITS['x_max'] or
                current[1] < WORKSPACE_LIMITS['y_min'] or current[1] > WORKSPACE_LIMITS['y_max'] or
                current[2] < WORKSPACE_LIMITS['z_min'] or current[2] > WORKSPACE_LIMITS['z_max']):
                print("\n  ВНИМАНИЕ: Робот находится ВНЕ допустимой зоны!")
    else:
        print("\nПроверка рабочей зоны отключена")
    
    print("\n" + "=" * 60)


def set_workspace_limits():
    """Установить новые ограничения рабочей зоны"""
    print("\n" + "=" * 60)
    print("УСТАНОВКА ОГРАНИЧЕНИЙ РАБОЧЕЙ ЗОНЫ")
    print("=" * 60)
    
    print("\nТекущие пределы:")
    print("  X: " + format(WORKSPACE_LIMITS['x_min'], ".0f") + " ... " + format(WORKSPACE_LIMITS['x_max'], ".0f"))
    print("  Y: " + format(WORKSPACE_LIMITS['y_min'], ".0f") + " ... " + format(WORKSPACE_LIMITS['y_max'], ".0f"))
    print("  Z: " + format(WORKSPACE_LIMITS['z_min'], ".0f") + " ... " + format(WORKSPACE_LIMITS['z_max'], ".0f"))
    
    print("\nВведите новые пределы (Enter - оставить без изменений):")
    
    try:
        x_min = input("X min (" + format(WORKSPACE_LIMITS['x_min'], ".0f") + "): ")
        if x_min != "":
            WORKSPACE_LIMITS['x_min'] = float(x_min)
        
        x_max = input("X max (" + format(WORKSPACE_LIMITS['x_max'], ".0f") + "): ")
        if x_max != "":
            WORKSPACE_LIMITS['x_max'] = float(x_max)
        
        y_min = input("Y min (" + format(WORKSPACE_LIMITS['y_min'], ".0f") + "): ")
        if y_min != "":
            WORKSPACE_LIMITS['y_min'] = float(y_min)
        
        y_max = input("Y max (" + format(WORKSPACE_LIMITS['y_max'], ".0f") + "): ")
        if y_max != "":
            WORKSPACE_LIMITS['y_max'] = float(y_max)
        
        z_min = input("Z min (" + format(WORKSPACE_LIMITS['z_min'], ".0f") + "): ")
        if z_min != "":
            WORKSPACE_LIMITS['z_min'] = float(z_min)
        
        z_max = input("Z max (" + format(WORKSPACE_LIMITS['z_max'], ".0f") + "): ")
        if z_max != "":
            WORKSPACE_LIMITS['z_max'] = float(z_max)
        
        print("\nНовые ограничения сохранены")
    except ValueError:
        print("Ошибка: введите число")
    
    show_workspace_limits()


def toggle_workspace_check():
    """Включить/выключить проверку рабочей зоны"""
    global WORKSPACE_CHECK_ENABLED
    WORKSPACE_CHECK_ENABLED = not WORKSPACE_CHECK_ENABLED
    print("\nПроверка рабочей зоны " + ("ВКЛЮЧЕНА" if WORKSPACE_CHECK_ENABLED else "ВЫКЛЮЧЕНА"))


# ============================================
# ОСТАЛЬНЫЕ ФУНКЦИИ (диагностика, движение и т.д.)
# ============================================

def full_diagnostics():
    """Полная диагностика состояния робота"""
    print("\n" + "=" * 60)
    print("ПОЛНАЯ ДИАГНОСТИКА РОБОТА")
    print("=" * 60)
    
    # Версии ПО
    print("\n1. ВЕРСИИ ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ:")
    # SDK: GetSoftwareVersion - получение версий ПО (модель, web, контроллер)
    error, model, web_ver, ctrl_ver = robot.GetSoftwareVersion()
    if error == 0:
        print("   Модель: " + str(model))
        print("   Web версия: " + str(web_ver))
        print("   Контроллер версия: " + str(ctrl_ver))
    
    # Состояние безопасности
    print("\n2. СОСТОЯНИЕ БЕЗОПАСНОСТИ:")
    # SDK: GetRobotEmergencyStopState - проверка аварийной остановки
    error, estop = robot.GetRobotEmergencyStopState()
    if error == 0:
        print("   Аварийная остановка: " + ("АКТИВНА" if estop == 1 else "НЕ АКТИВНА"))
    
    # SDK: GetSafetyStopState - проверка безопасного останова (ограждения)
    error, [si0, si1] = robot.GetSafetyStopState()
    if error == 0:
        print("   SI0 (ограждение): " + ("АКТИВЕН" if si0 == 1 else "НОРМА"))
        print("   SI1 (доп. защита): " + ("АКТИВЕН" if si1 == 1 else "НОРМА"))
    
    # Сервоприводы
    print("\n3. СОСТОЯНИЕ СЕРВОПРИВОДОВ:")
    # SDK: GetRobotRealTimeState - получение полного состояния робота
    error, state_pkg = robot.GetRobotRealTimeState()
    if error == 0:
        print("   Сервоприводы: " + ("ВКЛЮЧЕНЫ" if state_pkg.rbtEnableState == 1 else "ВЫКЛЮЧЕНЫ"))
        print("   Режим: " + ("АВТОМАТИЧЕСКИЙ" if state_pkg.robot_mode == 0 else "РУЧНОЙ"))
    
    # Ошибки
    print("\n4. КОДЫ ОШИБОК КОНТРОЛЛЕРА:")
    # SDK: GetRobotErrorCode - получение кодов ошибок контроллера
    error, [main, sub] = robot.GetRobotErrorCode()
    if error == 0:
        if main == 0:
            print("   Ошибок нет")
        else:
            print("   Главный код: " + str(main) + "  Подкод: " + str(sub))
    
    # Температура
    print("\n5. ТЕМПЕРАТУРА ДРАЙВЕРОВ (C):")
    # SDK: GetJointDriverTemperature - получение температуры драйверов
    error, temps = robot.GetJointDriverTemperature()
    if error == 0:
        print("   J1: " + format(temps[0], "6.1f") + "    J4: " + format(temps[3], "6.1f"))
        print("   J2: " + format(temps[1], "6.1f") + "    J5: " + format(temps[4], "6.1f"))
        print("   J3: " + format(temps[2], "6.1f") + "    J6: " + format(temps[5], "6.1f"))
    
    # Программные пределы суставов
    print("\n6. ПРОГРАММНЫЕ ПРЕДЕЛЫ СУСТАВОВ:")
    # SDK: GetJointSoftLimitDeg - получение мягких лимитов суставов
    error, limits = robot.GetJointSoftLimitDeg()
    if error == 0:
        print("   J1: [" + format(limits[0], "6.1f") + ", " + format(limits[1], "6.1f") + "]")
        print("   J2: [" + format(limits[2], "6.1f") + ", " + format(limits[3], "6.1f") + "]")
        print("   J3: [" + format(limits[4], "6.1f") + ", " + format(limits[5], "6.1f") + "]")
    
    # Текущее положение
    print("\n7. ТЕКУЩИЕ УГЛЫ СУСТАВОВ (градусы):")
    # SDK: GetActualJointPosDegree - получение текущих углов суставов
    error, joints = robot.GetActualJointPosDegree()
    if error == 0:
        print("   J1=" + format(joints[0], "7.2f") + "  J2=" + format(joints[1], "7.2f") + "  J3=" + format(joints[2], "7.2f"))
        print("   J4=" + format(joints[3], "7.2f") + "  J5=" + format(joints[4], "7.2f") + "  J6=" + format(joints[5], "7.2f"))
    
    # Информация о рабочей зоне
    print("\n8. РАБОЧАЯ ЗОНА:")
    print("   Проверка зоны: " + ("ВКЛ" if WORKSPACE_CHECK_ENABLED else "ВЫКЛ"))
    if WORKSPACE_CHECK_ENABLED:
        print("   X: " + format(WORKSPACE_LIMITS['x_min'], ".0f") + "..." + format(WORKSPACE_LIMITS['x_max'], ".0f"))
        print("   Y: " + format(WORKSPACE_LIMITS['y_min'], ".0f") + "..." + format(WORKSPACE_LIMITS['y_max'], ".0f"))
        print("   Z: " + format(WORKSPACE_LIMITS['z_min'], ".0f") + "..." + format(WORKSPACE_LIMITS['z_max'], ".0f"))
    
    print("\n" + "=" * 60)
    print("ДИАГНОСТИКА ЗАВЕРШЕНА")
    print("=" * 60)


def get_versions():
    """Информация о версиях"""
    print("\nВЕРСИИ ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ")
    # SDK: GetSoftwareVersion - получение версий ПО
    error, model, web_ver, ctrl_ver = robot.GetSoftwareVersion()
    if error == 0:
        print("  Модель: " + str(model))
        print("  Web версия: " + str(web_ver))
        print("  Контроллер версия: " + str(ctrl_ver))
    
    # SDK: GetFirmwareVersion - получение версий прошивок драйверов
    error, ctrl_fw, j1, j2, j3, j4, j5, j6, end = robot.GetFirmwareVersion()
    if error == 0:
        print("\nВЕРСИИ ПРОШИВОК:")
        print("  Контроллер: " + str(ctrl_fw))
        print("  J1:" + str(j1) + "  J2:" + str(j2) + "  J3:" + str(j3))
        print("  J4:" + str(j4) + "  J5:" + str(j5) + "  J6:" + str(j6))


def get_joint_limits():
    """Программные пределы суставов"""
    print("\nПРОГРАММНЫЕ ПРЕДЕЛЫ СУСТАВОВ")
    # SDK: GetJointSoftLimitDeg - получение мягких лимитов суставов
    error, limits = robot.GetJointSoftLimitDeg()
    if error == 0:
        print("\n  J1: от " + format(limits[0], "6.1f") + " до " + format(limits[1], "6.1f") + " град")
        print("  J2: от " + format(limits[2], "6.1f") + " до " + format(limits[3], "6.1f") + " град")
        print("  J3: от " + format(limits[4], "6.1f") + " до " + format(limits[5], "6.1f") + " град")
        print("  J4: от " + format(limits[6], "6.1f") + " до " + format(limits[7], "6.1f") + " град")
        print("  J5: от " + format(limits[8], "6.1f") + " до " + format(limits[9], "6.1f") + " град")
        print("  J6: от " + format(limits[10], "6.1f") + " до " + format(limits[11], "6.1f") + " град")


def reset_errors():
    """Сброс ошибок"""
    print("\nСБРОС ОШИБОК")
    confirm = input("Вы уверены? (Y/N): ").strip().lower()
    if confirm in ['y', 'yes', 'д', 'да']:
        # SDK: ResetAllError - сброс всех ошибок контроллера
        robot.ResetAllError()
        time.sleep(0.5)
        print("Ошибки сброшены")


def enable_servo():
    """Включение сервоприводов"""
    print("\nВКЛЮЧЕНИЕ СЕРВОПРИВОДОВ")
    # SDK: RobotEnable - включение/выключение сервоприводов (1-вкл, 0-выкл)
    robot.RobotEnable(1)
    time.sleep(0.5)
    print("Сервоприводы включены")


def disable_servo():
    """Выключение сервоприводов"""
    print("\nВЫКЛЮЧЕНИЕ СЕРВОПРИВОДОВ")
    # SDK: RobotEnable - включение/выключение сервоприводов (1-вкл, 0-выкл)
    robot.RobotEnable(0)
    print("Сервоприводы выключены")


def set_manual_mode():
    """Ручной режим"""
    # SDK: Mode - установка режима работы (0-автоматический, 1-ручной)
    robot.Mode(1)
    print("Ручной режим активирован")


def set_auto_mode():
    """Автоматический режим"""
    # SDK: Mode - установка режима работы (0-автоматический, 1-ручной)
    robot.Mode(0)
    print("Автоматический режим активирован")


def go_home(speed=15.0):
    """Возврат в исходное положение"""
    print("\nВОЗВРАТ В ИСХОДНОЕ ПОЛОЖЕНИЕ")
    home_pos = [0.0, -90.0, 90.0, 0.0, 90.0, 0.0]
    
    try:
        # SDK: MoveJ - движение по суставам (joint_pos, tool, user, vel, blendT)
        error = robot.MoveJ(home_pos, CURRENT_TOOL, CURRENT_WOBJ, vel=speed, blendT=-1.0)
        if error != 0:
            print("Ошибка: " + str(error))
            return False
        
        print("Движение...", end="", flush=True)
        # SDK: GetRobotMotionDone - проверка завершения движения (0-движется, 1-завершено)
        while True:
            err, done = robot.GetRobotMotionDone()
            if done == 1:
                break
            time.sleep(0.1)
        print(" Готово")
        return True
    except Exception as e:
        print("Ошибка: " + str(e))
        return False


def get_current_position():
    """Текущее положение"""
    print("\nТЕКУЩЕЕ ПОЛОЖЕНИЕ")
    # SDK: GetActualJointPosDegree - получение текущих углов суставов
    error, joints = robot.GetActualJointPosDegree()
    if error == 0:
        print("\nУГЛЫ СУСТАВОВ:")
        for i in range(6):
            print("  J" + str(i+1) + ": " + format(joints[i], "8.2f") + "°")
    
    # SDK: GetActualTCPPose - получение текущей позиции инструмента в пространстве
    error, tcp = robot.GetActualTCPPose()
    if error == 0:
        print("\nПОЛОЖЕНИЕ ИНСТРУМЕНТА:")
        print("  X: " + format(tcp[0], "8.2f") + " мм")
        print("  Y: " + format(tcp[1], "8.2f") + " мм")
        print("  Z: " + format(tcp[2], "8.2f") + " мм")

    show_current_bases()
    return True


def move_ptp_single():
    """Движение в одну точку с проверкой"""
    print("\nДВИЖЕНИЕ В ТОЧКУ (с проверкой)")
    
    # SDK: GetActualJointPosDegree - получение текущих углов суставов
    error, current = robot.GetActualJointPosDegree()
    if error == 0:
        print("\nТекущее положение:")
        print("  J1=" + format(current[0], ".1f") + "  J2=" + format(current[1], ".1f") + "  J3=" + format(current[2], ".1f"))
    
    print("\nВведите целевые углы суставов (градусы):")
    target = []
    for i in range(6):
        while True:
            try:
                val = input("  J" + str(i+1) + ": ")
                if val == "":
                    val = str(current[i])
                target.append(float(val))
                break
            except ValueError:
                print("   Ошибка: введите число")
    
    speed = 15.0
    print("\nЦелевое положение:")
    for i in range(6):
        print("  J" + str(i+1) + "=" + format(target[i], ".1f"))
    
    confirm = input("\nВыполнить движение? (Y/N): ").strip().lower()
    if confirm not in ['y', 'yes', 'д', 'да']:
        print("Отменено")
        return
    
    try:
        print("Движение...", end="", flush=True)
        # SDK: MoveJ - движение по суставам
        error = robot.MoveJ(target, CURRENT_TOOL, CURRENT_WOBJ, vel=speed, blendT=-1.0)
        if error != 0:
            print(" Ошибка: " + str(error))
            return
        
        # SDK: GetRobotMotionDone - проверка завершения движения
        while True:
            err, done = robot.GetRobotMotionDone()
            if done == 1:
                break
            time.sleep(0.1)
        print(" Готово")
    except Exception as e:
        print(" Ошибка: " + str(e))


def move_ptp_array():
    """Движение по массиву точек с проверкой достижимости"""
    print("\nДВИЖЕНИЕ ПО МАССИВУ ТОЧЕК")
    
    print("Введите количество точек:")
    while True:
        try:
            num_points = int(input("Число точек: "))
            if num_points > 0:
                break
        except ValueError:
            print("Ошибка: введите целое число")
    
    points = []
    print("\nВведите углы для каждой точки (6 значений J1-J6 через пробел):")
    
    for i in range(num_points):
        print("\nТочка " + str(i+1) + ":")
        while True:
            try:
                values = input("  J1 J2 J3 J4 J5 J6: ").split()
                if len(values) != 6:
                    print("  Нужно 6 значений")
                    continue
                point = [float(v) for v in values]
                points.append(point)
                break
            except ValueError:
                print("  Ошибка: введите числа")
    
    speed = 15.0
    
    print("\nПРОВЕРКА ДОСТИЖИМОСТИ ТОЧЕК:")
    for i, point in enumerate(points):
        if check_point_safe(point):
            print("  Точка " + str(i+1) + ": ДОСТИЖИМА")
        else:
            print("  Точка " + str(i+1) + ": НЕДОСТИЖИМА")
            confirm = input("Пропустить эту точку? (Y/N): ").strip().lower()
            if confirm in ['y', 'yes', 'д', 'да']:
                continue
            else:
                print("Движение отменено")
                return
    
    confirm = input("\nВыполнить движение по достижимым точкам? (Y/N): ").strip().lower()
    if confirm not in ['y', 'yes', 'д', 'да']:
        print("Отменено")
        return
    
    for i, target in enumerate(points):
        if not check_point_safe(target):
            print("\nТочка " + str(i+1) + " пропущена (недостижима)")
            continue
        
        print("\n--- Точка " + str(i+1) + " ---")
        try:
            # SDK: MoveJ - движение по суставам
            error = robot.MoveJ(target, CURRENT_TOOL, CURRENT_WOBJ, vel=speed, blendT=-1.0)
            if error != 0:
                print("  Ошибка: " + str(error))
                continue
            
            print("  Движение...", end="", flush=True)
            # SDK: GetRobotMotionDone - проверка завершения движения
            while True:
                err, done = robot.GetRobotMotionDone()
                if done == 1:
                    break
                time.sleep(0.1)
            print(" Готово")
        except Exception as e:
            print("  Ошибка: " + str(e))
    
    print("\nДвижение завершено")


def rotate_joint():
    """Поворот сустава на N градусов с проверкой"""
    print("\nПОВОРОТ СУСТАВА")
    
    print("Выберите сустав (1-6):")
    while True:
        try:
            joint = int(input("Номер: "))
            if 1 <= joint <= 6:
                break
        except ValueError:
            pass
        print("Ошибка: введите 1-6")
    
    print("Направление: 1 - положительное, 2 - отрицательное")
    while True:
        try:
            direction = int(input("Направление: "))
            if direction in [1, 2]:
                break
        except ValueError:
            pass
        print("Ошибка: введите 1 или 2")
    
    while True:
        try:
            angle = float(input("Угол поворота (1-360): "))
            if 0 < angle <= 360:
                break
        except ValueError:
            pass
        print("Ошибка: введите число")
    
    if direction == 2:
        angle = -angle
    
    # SDK: GetActualJointPosDegree - получение текущих углов суставов
    error, current = robot.GetActualJointPosDegree()
    if error != 0:
        print("Ошибка получения позиции")
        return
    
    new_pos = current.copy()
    new_pos[joint - 1] = current[joint - 1] + angle
    
    print("\nИнформация:")
    print("  Текущий: " + format(current[joint-1], ".1f") + "°")
    print("  Поворот: " + format(angle, ".1f") + "°")
    print("  Новый:   " + format(new_pos[joint-1], ".1f") + "°")
    
    confirm = input("Выполнить? (Y/N): ").strip().lower()
    if confirm not in ['y', 'yes', 'д', 'да']:
        print("Отменено")
        return
    
    try:
        print("Движение...", end="", flush=True)
        # SDK: MoveJ - движение по суставам
        error = robot.MoveJ(new_pos, CURRENT_TOOL, CURRENT_WOBJ, vel=15.0, blendT=-1.0)
        if error != 0:
            print("Ошибка: " + str(error))
            return
        
        # SDK: GetRobotMotionDone - проверка завершения движения
        while True:
            err, done = robot.GetRobotMotionDone()
            if done == 1:
                break
            time.sleep(0.1)
        print(" Готово")
    except Exception as e:
        print("Ошибка: " + str(e))


def show_error_reference():
    """Справка по ошибкам"""
    print("\n" + "=" * 70)
    print("СПРАВКА ПО КОДАМ ОШИБОК")
    print("=" * 70)
    
    errors = {
        -4: "Нет связи с контроллером",
        -2: "Ошибка сокета",
        -1: "Общая ошибка",
        14: "Ошибка файла (MoveL требует загрузки программы)",
        74: "Невозможно построить траекторию",
        112: "Недопустимая конфигурация для MoveL",
        185: "Конфликт конфигурации (используйте MoveJ)",
        1001: "Столкновение",
        1004: "Ошибка следования (снизьте скорость)",
        2001: "Мягкий лимит (вернитесь в зону)",
        2002: "Жесткий лимит (ручное возвращение)",
        3001: "Ошибка сервопривода J1",
        3002: "Ошибка сервопривода J2",
        3003: "Ошибка сервопривода J3",
        3004: "Ошибка сервопривода J4",
        3005: "Ошибка сервопривода J5",
        3006: "Ошибка сервопривода J6",
        4001: "Ошибка EtherCAT связи",
        5001: "Аварийная остановка (E-Stop)",
        5002: "Безопасный останов (ограждение)",
        6001: "Ошибка питания 24V",
        6002: "Ошибка питания 220V",
    }
    
    for code, desc in sorted(errors.items()):
        print("  " + format(code, "4d") + " : " + desc)
    
    print("\n" + "=" * 70)
    input("Нажмите Enter...")


def move_ptp_with_check():
    """Движение в точку с полной проверкой (достижимость + зона)"""
    print("\nДВИЖЕНИЕ В ТОЧКУ (с полной проверкой)")
    
    print("\nВведите целевые координаты TCP (X, Y, Z):")
    try:
        x = float(input("X (мм): "))
        y = float(input("Y (мм): "))
        z = float(input("Z (мм): "))
        rx = float(input("Rx (град, Enter=0): ") or "0")
        ry = float(input("Ry (град, Enter=0): ") or "0")
        rz = float(input("Rz (град, Enter=0): ") or "0")
    except ValueError:
        print("Ошибка ввода")
        return
    
    target_point = [x, y, z, rx, ry, rz]
    
    print("\nЦелевая точка:")
    print("  X=" + format(x, ".1f") + "  Y=" + format(y, ".1f") + "  Z=" + format(z, ".1f"))
    
    # Проверка рабочей зоны
    if WORKSPACE_CHECK_ENABLED:
        print("\nПРОВЕРКА РАБОЧЕЙ ЗОНЫ...")
        if not is_point_in_workspace(target_point):
            print("Точка ВНЕ рабочей зоны!")
            return
        print("  Точка в рабочей зоне")
    
    # Проверка достижимости
    print("ПРОВЕРКА ДОСТИЖИМОСТИ...")
    if not is_point_reachable(target_point):
        print("Точка НЕДОСТИЖИМА!")
        return
    print("  Точка достижима")
    
    # SDK: GetInverseKin - решение обратной кинематики (получение углов по координатам)
    error, joints = robot.GetInverseKin(0, target_point)
    if error != 0:
        print("Ошибка обратной кинематики: " + str(error))
        return
    
    print("\nНайденное решение по углам:")
    for i in range(6):
        print("  J" + str(i+1) + "=" + format(joints[i], ".1f"))
    
    confirm = input("\nВыполнить движение? (Y/N): ").strip().lower()
    if confirm not in ['y', 'yes', 'д', 'да']:
        print("Отменено")
        return
    
    try:
        print("Движение...", end="", flush=True)
        # SDK: MoveJ - движение по суставам
        error = robot.MoveJ(joints, CURRENT_TOOL, CURRENT_WOBJ, vel=15.0, blendT=-1.0)
        if error != 0:
            print(" Ошибка: " + str(error))
            return
        
        # SDK: GetRobotMotionDone - проверка завершения движения
        while True:
            err, done = robot.GetRobotMotionDone()
            if done == 1:
                break
            time.sleep(0.1)
        print(" Готово")
    except Exception as e:
        print(" Ошибка: " + str(e))

def move_ptp_array_by_coords():
    """Движение по массиву точек (по координатам X,Y,Z с проверкой)"""
    print("\n" + "=" * 60)
    print("ДВИЖЕНИЕ ПО МАССИВУ ТОЧЕК (по координатам)")
    print("=" * 60)
    
    print("Введите количество точек:")
    while True:
        try:
            num_points = int(input("Число точек: "))
            if num_points > 0:
                break
        except ValueError:
            print("Ошибка: введите целое число")
    
    points = []
    print("\nВведите координаты для каждой точки (X, Y, Z, Rx, Ry, Rz):")
    print("  Rx, Ry, Rz - ориентация инструмента (градусы), Enter=0")
    
    for i in range(num_points):
        print("\nТочка " + str(i+1) + ":")
        try:
            x = float(input("  X (мм): "))
            y = float(input("  Y (мм): "))
            z = float(input("  Z (мм): "))
            rx = float(input("  Rx (град, Enter=0): ") or "0")
            ry = float(input("  Ry (град, Enter=0): ") or "0")
            rz = float(input("  Rz (град, Enter=0): ") or "0")
            points.append([x, y, z, rx, ry, rz])
        except ValueError:
            print("  Ошибка ввода! Точка пропущена")
            continue
    
    if len(points) == 0:
        print("Нет корректных точек для движения")
        return
    
    while True:
        try:
            speed_input = input("\nВведите скорость (0-100%, Enter=15): ")
            if speed_input == "":
                speed = 15.0
            else:
                speed = float(speed_input)
            if 0 <= speed <= 100:
                break
        except ValueError:
            pass
        print("Ошибка: введите 0-100")
    
    print("\nПРОВЕРКА ДОСТИЖИМОСТИ ТОЧЕК:")
    reachable_points = []
    
    for i, point in enumerate(points):
        print("\nТочка " + str(i+1) + ": X=" + format(point[0], ".1f") + 
              " Y=" + format(point[1], ".1f") + " Z=" + format(point[2], ".1f"))
        
        # Проверка рабочей зоны
        if WORKSPACE_CHECK_ENABLED:
            if not is_point_in_workspace(point):
                print("  НЕДОСТИЖИМА (вне рабочей зоны)")
                confirm = input("  Пропустить? (Y/N): ").strip().lower()
                if confirm in ['y', 'yes', 'д', 'да']:
                    continue
                else:
                    print("Движение отменено")
                    return
        
        # Проверка достижимости
        if not is_point_reachable(point):
            print("  НЕДОСТИЖИМА (нет решения обратной кинематики)")
            confirm = input("  Пропустить? (Y/N): ").strip().lower()
            if confirm in ['y', 'yes', 'д', 'да']:
                continue
            else:
                print("Движение отменено")
                return
        
        # Получаем углы через обратную кинематику
        error, joints = robot.GetInverseKin(0, point)
        if error != 0:
            print("  Ошибка обратной кинематики: " + str(error))
            continue
        
        print("  ДОСТИЖИМА")
        reachable_points.append(joints)
    
    if len(reachable_points) == 0:
        print("\nНет достижимых точек для движения")
        return
    
    confirm = input("\nВыполнить движение по " + str(len(reachable_points)) + " достижимым точкам? (Y/N): ").strip().lower()
    if confirm not in ['y', 'yes', 'д', 'да']:
        print("Отменено")
        return
    
    print("\n" + "=" * 60)
    print("НАЧАЛО ДВИЖЕНИЯ")
    print("=" * 60)
    
    for i, joints in enumerate(reachable_points):
        print("\n--- Точка " + str(i+1) + " из " + str(len(reachable_points)) + " ---")
        print("  Углы: J1=" + format(joints[0], ".1f") + " J2=" + format(joints[1], ".1f") + " J3=" + format(joints[2], ".1f"))
        
        try:
            error = robot.MoveJ(joints, CURRENT_TOOL, CURRENT_WOBJ, vel=speed, blendT=-1.0)
            if error != 0:
                print("  Ошибка: " + str(error))
                continue
            
            print("  Движение...", end="", flush=True)
            while True:
                err, done = robot.GetRobotMotionDone()
                if done == 1:
                    break
                time.sleep(0.1)
            print(" Готово")
        except Exception as e:
            print("  Ошибка: " + str(e))
    
    print("\nДвижение завершено")
# ============================================
# ГЛАВНОЕ МЕНЮ
# ============================================

def show_menu():
    print("\n" + "=" * 60)
    print("ГЛАВНОЕ МЕНЮ УПРАВЛЕНИЯ РОБОТОМ")
    print("=" * 60)
    print("  ДИАГНОСТИКА:")
    print("    1 - Полная диагностика")
    print("    2 - Текущее положение")
    print("    3 - Версии ПО")
    print("    4 - Пределы суставов")
    print("    5 - Справка по ошибкам")
    print("")
    print("  БАЗИСЫ (инструменты и координаты):")
    print("    6 - Показать текущие базисы")
    print("    7 - Выбрать инструмент для движения")
    print("    8 - Выбрать систему координат для движения")
    print("    9 - Список инструментов (1-14)")
    print("    10 - Список систем координат (1-14)")
    print("    11 - Настроить инструмент")
    print("    12 - Настроить систему координат")
    print("    13 - Сбросить инструмент в 0")
    print("    14 - Сбросить систему координат в 0")
    print("")
    print("  РАБОЧАЯ ЗОНА:")
    print("    15 - Показать/настроить зону")
    print("    16 - Включить/выключить проверку зоны")
    print("")
    print("  УПРАВЛЕНИЕ:")
    print("    17 - Включить сервоприводы")
    print("    18 - Выключить сервоприводы")
    print("    19 - Ручной режим")
    print("    20 - Автоматический режим")
    print("    21 - Сброс ошибок")
    print("")
    print("  ДВИЖЕНИЕ:")
    print("    22 - Домой")
    print("    23 - Повернуть сустав")
    print("    24 - PTP (одна точка по углам)")
    print("    25 - PTP (массив точек по углам )")
    print("    26 - PTP (одна точка по координатам)")
    print("    27 - PTP (массив точек по координатам)")
    print("")
    print("    0 - Выход")
    print("=" * 60)


def main():
    print("\nУПРАВЛЕНИЕ РОБОТОМ v3.0")
    
    while True:
        show_menu()
        choice = input("Выберите действие (0-27): ").strip()
        
        if choice == "0":
            print("Завершение работы")
            break
        
        elif choice == "1": full_diagnostics()
        elif choice == "2": get_current_position()
        elif choice == "3": get_versions()
        elif choice == "4": get_joint_limits()
        elif choice == "5": show_error_reference()
        
        elif choice == "6": show_current_bases()
        elif choice == "7": select_current_tool()
        elif choice == "8": select_current_wobj()
        elif choice == "9": show_all_tools()
        elif choice == "10": show_all_wobjs()
        elif choice == "11": configure_tool()
        elif choice == "12": configure_wobj()
        elif choice == "13": reset_tool()
        elif choice == "14": reset_wobj()
        
        elif choice == "15": 
            print("\n1 - Показать зону")
            print("2 - Настроить зону")
            sub = input("Выберите: ")
            if sub == "1": show_workspace_limits()
            elif sub == "2": set_workspace_limits()
            else: print("Неверный выбор")
        
        elif choice == "16": toggle_workspace_check()
        elif choice == "17": enable_servo()
        elif choice == "18": disable_servo()
        elif choice == "19": set_manual_mode()
        elif choice == "20": set_auto_mode()
        elif choice == "21": reset_errors()
        elif choice == "22": go_home()
        elif choice == "23": rotate_joint()
        elif choice == "24": move_ptp_single()
        elif choice == "25": move_ptp_array()
        elif choice == "26": move_ptp_with_check()
        elif choice == "27": move_ptp_array_by_coords()
        
        else:
            print("Ошибка: введите 0-27")
        
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрервано")
        # SDK: StopMotion - аварийная остановка всех движений
        robot.StopMotion()