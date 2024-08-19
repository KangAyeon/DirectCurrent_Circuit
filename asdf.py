import tkinter as tk

def show_focus_widget():
    focused_widget = root.focus_get()
    if focused_widget:
        print(f"현재 포커스를 받고 있는 위젯: {focused_widget}")
        print(type(focused_widget))
    else:
        print("포커스를 받고 있는 위젯이 없습니다.")

root = tk.Tk()
entry1 = tk.Entry(root)
entry2 = tk.Entry(root)
button = tk.Button(root, text="포커스 확인", command=show_focus_widget)

entry1.pack()
entry2.pack()
button.pack()

root.mainloop()
