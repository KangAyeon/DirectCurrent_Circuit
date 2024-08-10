import tkinter as tk
from tkinter import ttk #as as as as as as as eefsd as as as sdf asdf asdf sdf df f df sdf asdf asdf sdf df f df


root = tk.Tk()
root.title("읽기 전용 Spinbox")

spinbox = ttk.Spinbox(root, from_=0, to=100, state='readonly')
spinbox.set(0)  # 초기값 설정
spinbox.pack(padx=10, pady=10)


root.mainloop()