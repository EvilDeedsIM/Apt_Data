import tkinter as tk
from tkinter import messagebox
import sys
import pystray
from PIL import Image
from io import BytesIO
import base64
from pystray import MenuItem as item

# Глобальная переменная для иконки в трее
tray_icon = None

# Встроенная иконка в формате base64 (замените на вашу строку)
ICON_BASE64 = """
iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABYSURBVDhPY2AYBaNgFIyCUTAKRsEoGAWjYBSMglEwCkbBKBgFo2AUjIJRMApGwSgYBaNgFIyCUTAKRsEoGAWjYBSMglEwCkbBKBgFo2AUjIJRMApGwQDvLBaD7WvWlwAAAABJRU5ErkJggg==
"""  # Это пример, замените на свою строку

# Функция обратного отсчёта
def countdown(time_in_seconds):
    def update_timer():
        nonlocal time_in_seconds
        if time_in_seconds > 0:
            mins, secs = divmod(time_in_seconds, 60)
            label.config(text=f"{mins:02}:{secs:02}")
            time_in_seconds -= 1
            root.after(1000, update_timer)
        else:
            show_end_dialog()

    update_timer()

# Функция показа диалогового окна по окончании времени
def show_end_dialog():
    dialog = tk.Toplevel(root)
    dialog.geometry("200x100")
    dialog.overrideredirect(True)
    dialog.attributes("-topmost", True)
    dialog.config(bg="black")
    
    x = root.winfo_x() + (root.winfo_width() - 200) // 2
    y = root.winfo_y() + (root.winfo_height() - 100) // 2
    dialog.geometry(f"+{x}+{y}")

    msg = tk.Label(dialog, text="60 минут истекли!", fg="white", bg="black")
    msg.pack(pady=10)

    button_frame = tk.Frame(dialog, bg="black")
    button_frame.pack(pady=10)

    close_btn = tk.Button(button_frame, text="Close", 
                         command=lambda: sys.exit(0),
                         fg="white", bg="gray30")
    close_btn.pack(side=tk.LEFT, padx=5)

    restart_btn = tk.Button(button_frame, text="Restart",
                           command=lambda: [dialog.destroy(), restart_timer()],
                           fg="white", bg="gray30")
    restart_btn.pack(side=tk.LEFT, padx=5)

    dialog.bind('<Escape>', lambda event: sys.exit(0))
    dialog.bind('<F1>', lambda event: [dialog.destroy(), restart_timer()])
    dialog.focus_set()

# Функция перезапуска таймера
def restart_timer():
    label.config(text="60:00")
    countdown(60 * 60)

# Функция для начала перетаскивания окна
def start_drag(event):
    root.x_offset = event.x_root
    root.y_offset = event.y_root

# Функция для перемещения окна
def drag_window(event):
    delta_x = event.x_root - root.x_offset
    delta_y = event.y_root - root.y_offset
    root.geometry(f"+{root.winfo_x() + delta_x}+{root.winfo_y() + delta_y}")
    root.x_offset = event.x_root
    root.y_offset = event.y_root

# Функция для сворачивания в трей
def minimize_to_tray():
    root.withdraw()
    create_tray_icon()

# Функция для восстановления окна
def restore_from_tray(icon, item):
    icon.stop()
    root.deiconify()

# Функция для закрытия приложения из трея
def quit_from_tray(icon, item):
    icon.stop()
    root.quit()
    sys.exit(0)

# Создание иконки в системном трее
def create_tray_icon():
    global tray_icon
    # Декодируем иконку из base64
    image_data = base64.b64decode(ICON_BASE64)
    image = Image.open(BytesIO(image_data))
    menu = (
        item('Restore', restore_from_tray),
        item('Quit', quit_from_tray)
    )
    tray_icon = pystray.Icon("Timer", image, "Timer App", menu)
    tray_icon.run()

# Создание основного окна
root = tk.Tk()
root.geometry("300x150")
root.overrideredirect(True)
root.attributes("-topmost", True)
root.config(bg='black')
root.attributes("-transparentcolor", "black")

# Создание текста таймера
label = tk.Label(root, text="60:00", font=("Helvetica", 32), fg="white", bg="black")
label.pack(expand=True)

# Обработчики для перетаскивания окна
label.bind("<Button-1>", start_drag)
label.bind("<B1-Motion>", drag_window)
label.bind("<Double-Button-1>", lambda event: minimize_to_tray())
root.bind('<Escape>', lambda event: quit_from_tray(None, None))

# Запуск таймера
countdown(60 * 60)

# Главный цикл приложения
root.mainloop()

# Уборка при закрытии
if tray_icon:
    tray_icon.stop()