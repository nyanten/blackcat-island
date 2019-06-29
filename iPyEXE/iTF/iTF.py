import os, sys, shutil
import tkinter as tk
import tkinter.filedialog as tkFD
import tkinter.messagebox as tkMB

root = tk.Tk()
root.resizable(width=False, height=False)
root.title("iTF")
root.geometry("255x110+100+100")


FILE_LIST = []

class Application(tk.Frame):
    def __init__(self, master=None):
        frame = tk.Frame.__init__(self, master)
        self.pack(expand=1, fill=tk.BOTH, anchor=tk.NW)
        self.create_widgets()
        self.listbox()
        self.place()

    # ウィジェット作成
    def create_widgets(self):
        self.frame_lb = tk.LabelFrame(root, text=u"path")
        self.button_open = tk.Button(self, text=u"開く", command=self.open, width=6)
        self.button_exit = tk.Button(self, text=u"終了", command=self.exit, width=4)
        self.button_transfer = tk.Button(self, text=u"変換", command=self.transfer, width=12)
        self.button_clear = tk.Button(self, text=u"クリア", command=self.clear, width=12)

    # リストボックス作成
    def listbox(self):
        argvs = tk.StringVar(value=FILE_LIST)
        self.listbox = tk.Listbox(self.frame_lb, listvariable=argvs, width=18, height=5, relief=tk.RIDGE, bd=2)
        self.scrollbar = tk.Scrollbar(self.frame_lb, orient="v", command=self.listbox.yview)
        self.listbox['yscrollcommand'] = self.scrollbar.set
        self.listbox.grid(row=0, column=0)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.listbox.bind("<Button-3>", self.one_clear)

    # 場所
    def place(self):
        self.frame_lb.place(x=7, y=1)
        self.button_open.place(x=150, y=70)
        self.button_exit.place(x=205, y=70)
        self.button_transfer.place(x=150, y=10)
        self.button_clear.place(x=150, y=40)

    # コマンド
    def open(self):
        global FILE_LIST
        file = tkFD.askopenfilenames(filetypes=[("any files", "")],initialdir=os.getcwd())
        if not file:
            print("Not Found...")
        else:
            FILE_LIST = list(file)
            add_list = list(file)
            for i in range(len(add_list)):
                sp = os.path.basename(add_list[i])
                add_list[i] = sp
            if bool(FILE_LIST) == False:
                for i in range(len(add_list)):
                    self.listbox.insert(tk.END, add_list[i])
            else:
                for i in range(len(add_list)):
                    self.listbox.insert(tk.END, add_list[i])

    # 終了
    def exit(self):
        print("exit")
        sys.exit()

    # くっつけ保存
    def transfer(self):
        if bool(FILE_LIST) == False:
            tkMB.showinfo("警告!", "ファイルを開いてください。")
        elif bool(self.listbox.curselection()) == True:
            file = tkFD.asksaveasfilename(filetypes=[("file name", "*.")],initialdir=os.path.join(os.getcwd(), "/append/"))

        else:
            return
            tkMB.showinfo("", "結合完了")
            
    # クリア
    def clear(self):
        global FILE_LIST
        print(len(FILE_LIST))
        for i in range(len(FILE_LIST)):
            self.listbox.delete(i, tk.END)
        FILE_LIST.clear()

    # ひとつだけクリア
    def one_clear(self, ls):
        global FILE_LIST
        for i in self.listbox.curselection():
            self.listbox.delete(i)
            del FILE_LIST[i]


if __name__ == '__main__':
    app = Application(master=root)
    app.pack()
    app.mainloop()
