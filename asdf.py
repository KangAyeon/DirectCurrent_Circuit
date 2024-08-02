import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200")

# 텍스트 위젯 생성
text = tk.Text(root, wrap="none")
text.place(x=10, y=10, width=260, height=150)

# 수직 스크롤바 생성
vscrollbar = ttk.Scrollbar(root, orient="vertical", command=text.yview)
vscrollbar.place(x=270, y=10, height=150)

# 수평 스크롤바 생성
hscrollbar = ttk.Scrollbar(root, orient="horizontal", command=text.xview)
hscrollbar.place(x=10, y=160, width=260)

# 스크롤바와 텍스트 위젯 연결
text.configure(yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)

root.mainloop()