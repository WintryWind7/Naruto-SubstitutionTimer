import pygetwindow as gw
import pyautogui
import time
import tkinter as tk
import time
import threading
import numpy as np


running = True
start_time = time.time()
all_time = 14.3
time_left = 0
Player = 1
reset_timer_flag = False  # 控制计时器重置的标志

def get_window_rect():
    target_window = gw.getWindowsWithTitle("雷电模拟器")[0]
    window_rect = target_window.left, target_window.top, target_window.width, target_window.height
    return window_rect

print(get_window_rect())
def get_img_t(lefttop, rightbottom, window_size):
    # 获取默认窗口大小
    default_window_left, default_window_top, default_window_right, default_window_bottom = 378, 115, 1962, 1115

    # 获取实际窗口大小
    window_left, window_top, window_right, window_bottom = window_size

    # 计算窗口比例
    kx = (window_right - window_left) / (default_window_right - default_window_left)
    ky = (window_bottom - window_top) / (default_window_bottom - default_window_top)

    # 计算实际区域的位置和大小
    left, top = lefttop
    right, bottom = rightbottom

    # 计算实际截图区域的左上角和右下角坐标
    left_pos = int(left * kx) + window_left
    top_pos = int(top * ky) + window_top
    right_pos = int(right * kx) + window_left
    bottom_pos = int(bottom * ky) + window_top

    # 截取指定区域的截图
    screenshot = pyautogui.screenshot(region=(left_pos, top_pos, right_pos - left_pos, bottom_pos - top_pos))
    screenshot.save('temp.png')

    return screenshot


def get_center_img(x, y, window_size, size):
    # 获取默认窗口大小
    default_window_left, default_window_top, default_window_right, default_window_bottom = 378, 115, 1962, 1115

    # 获取实际窗口大小
    window_left, window_top, window_right, window_bottom = window_size

    # 计算窗口比例
    kx = (window_right - window_left) / (default_window_right - default_window_left)
    ky = (window_bottom - window_top) / (default_window_bottom - default_window_top)

    # 计算实际坐标
    x_pos = int(window_left + x * kx)
    y_pos = int(window_top + y * ky)

    # 计算实际大小
    size_x = int(size * kx)
    size_y = int(size * ky)

    # 计算截图区域的左上角和右下角坐标
    left_pos = x_pos - size_x // 2
    top_pos = y_pos - size_y // 2
    right_pos = x_pos + size_x // 2
    bottom_pos = y_pos + size_y // 2

    # 截取指定区域的截图
    screenshot = pyautogui.screenshot(region=(left_pos, top_pos, size_x, size_y))
    screenshot.save('temp.png')

    return screenshot


def get_img(x, y, window_rect, radius=6):
    """
    截取屏幕上以 (x, y) 为中心的正方形区域，并返回该区域的NumPy数组格式的像素值。

    Args:
    x (int): 中心点的横坐标。
    y (int): 中心点的纵坐标。
    window_rect (tuple): 包含窗口位置和大小的元组，格式为 (x, y, width, height)。
    radius (int): 正方形区域的半径（中心到边缘的距离）。

    Returns:
    np.array: 返回的NumPy数组，包含截取区域的像素值。
    """
    # 解析窗口的位置和大小
    window_x, window_y, window_width, window_height = window_rect

    # 计算窗口比例（相对于默认值）
    default_width, default_height = 1962, 1115
    kx = window_width / default_width
    ky = window_height / default_height

    # 计算实际坐标
    x_pos = int(window_x + x * kx)
    y_pos = int(window_y + y * ky)

    # 计算截图区域的左上角和右下角坐标
    left = x_pos - radius
    top = y_pos - radius
    right = x_pos + radius
    bottom = y_pos + radius

    # 截取指定区域的屏幕
    img = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
    img.save('test.jpg')
    img_np = np.array(img)
    return img_np

count_temp = 2
num_up = 0
num_down = 0
def condition_met():
    global Player, count_temp, num_up, num_down
    try:
        window_rect = get_window_rect()
        if Player == 1:

            count = 0  # 初始化满足条件的区域计数
            ls1 = [get_img(x, 137, window_rect) for x in [178, 208, 238, 268]] # 188, 218, 248, 278
            count_list = []
            for area in ls1[:count_temp+1]:
                # 计算的是满足空豆情况的个数
                matching_pixels = np.sum((area[:, :, 0] < 70) & (area[:, :, 1] < 70) & (area[:, :, 2] < 120))
                if matching_pixels >= 144*0.85: # 30/36
                    count_list.append(0)
                    break
                else:
                    count_list.append(1)
            count = sum(count_list)
            print(count_list, count)
            if count < count_temp and num_down >2:
                count_temp = count
                num_up = 0
                print('p1替身了')
                return True
            elif count < count_temp:
                num_down += 1
            elif count > count_temp and num_up >3:
                count_temp = count
                num_up = 0
            elif count > count_temp:
                num_up += 1
        else:

            # 对第二个玩家进行相似的检查
            ls2 = [get_img(x, 137, window_rect) for x in (1731, 1701, 1671, 1641)]
            count = 0
            count_list = []
            for area in ls2[:count_temp+1]:
                # 计算每个区域中满足颜色条件的像素数量
                matching_pixels = np.sum((area[:, :, 0] < 70) & (area[:, :, 1] < 70) & (area[:, :, 2] < 120))
                if matching_pixels >= 144*0.85: # 30/36
                    count_list.append(0)
                    break
                else:
                    count_list.append(1)
            count = sum(count_list)
            print(count_list, count)
            # print(f'现在:{count}, 过去:{count_temp}')
            if count < count_temp and num_down > 2:
                count_temp = count
                num_up = 0
                print('p2替身了')
                return True
            elif count < count_temp:
                num_down += 1
            elif count > count_temp and num_up >3:
                count_temp = count
                num_up = 0
            elif count > count_temp:
                num_up += 1
    except Exception as e:
        print(f'未找到窗口或错误：{str(e)}')
    return False

def set_character_p1():
    global Player
    character_label.config(text="角色：p1")
    Player = 1

def set_character_p2():
    global Player
    character_label.config(text="角色：p2")
    Player = 2

def timer_thread():
    """持续计时的线程，负责更新剩余时间和显示"""
    global start_time, time_left, all_time
    while running:
        elapsed = time.time() - start_time
        time_left = all_time - elapsed
        if time_left > 0:
            timer_label.config(text=f"{time_left:.1f}")
        else:
            timer_label.config(text="替身好了!")
        time.sleep(0.1)



def control_thread():
    """根据条件重置 start_time 的线程"""
    global start_time
    while running:
        if condition_met():
            start_time = time.time()  # 重置开始时间
        time.sleep(0.1)  # 根据需要调整检查频率



root = tk.Tk()
root.title("计时器")

timer_label = tk.Label(root, text=f"{time_left:.1f}", font=("Helvetica", 24))
timer_label.pack(pady=20)

character_label = tk.Label(root, text="角色：", font=("Helvetica", 16))
character_label.pack(pady=10)

set_p1_button = tk.Button(root, text="设置角色为p1", command=set_character_p1)
set_p1_button.pack(side=tk.LEFT, padx=10)

set_p2_button = tk.Button(root, text="设置角色为p2", command=set_character_p2)
set_p2_button.pack(side=tk.RIGHT, padx=10)

# 创建并启动计时线程
t_timer = threading.Thread(target=timer_thread)
t_timer.start()

# 创建并启动控制线程
t_control = threading.Thread(target=control_thread)
t_control.start()

root.mainloop()




if __name__ == "__main__":
    root.mainloop()