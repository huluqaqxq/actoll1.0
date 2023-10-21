import tkinter as tk


def tk_init():
    window = tk.Tk()
    window.title('Actool1.01')
    return window


def disable_input(event):
    ''' 禁用键盘输入
    :param event:
    :return:
    '''
    return "break"


def get_text(window):
    text = tk.Text(window, width=600, height=400)
    # text.tag_configure("highlight", background="#FFFF00", foreground="#000000")
    text.tag_configure("highlight", background="#87CEFA", foreground="#000000")
    text.bind("<KeyPress>", disable_input)
    text.pack()
    return text
