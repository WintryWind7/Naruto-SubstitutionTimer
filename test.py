import tkinter as tk
from PIL import Image, ImageTk
import threading

running = True
time_left = 0

def update_image(label):
    """
    更新图像显示的函数。
    """
    try:
        img = Image.open('test.jpg')  # 打开图片文件
        img = img.resize((200, 200), Image.Resampling.LANCZOS)  # 调整图片大小
        photo = ImageTk.PhotoImage(img)  # 创建用于显示的图片对象
        label.config(image=photo)  # 更新标签上的图片
        label.image = photo  # 防止图片被垃圾收集器清除
    except IOError:
        print("Error updating image")
    root.after(1000, update_image, label)  # 每秒更新一次图片

def run_gui():
    global root
    root = tk.Tk()
    root.title("实时图片显示")

    img_label = tk.Label(root)
    img_label.pack()

    # 初始化图片更新
    update_image(img_label)

    root.mainloop()

if __name__ == "__main__":
    t_gui = threading.Thread(target=run_gui)
    t_gui.start()
