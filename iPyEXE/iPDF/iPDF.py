# coding: utf-8

import os, sys, shutil
import tkinter as tk
import tkinter.filedialog as tkFD
import tkinter.messagebox as tkMB
from PIL import Image
from PyPDF2 import PdfFileMerger, PdfFileReader
from pdf2image import convert_from_path
from io import BytesIO
#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.converter import TextConverter
#from pdfminer.layout import LAParams
#from pdfminer.pdfpage import PDFPage
#from io import StringIO

# Pyinstaller hoge.py -D -F -w

root = tk.Tk()
root.resizable(width=False, height=False)
root.title("iPDF")
root.geometry("400x200+100+100")


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
        # EXE化で必要な外部ファイル参照メソッド
        def resource_path(relative_path):
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.abspath("."), relative_path)

        # resource_pathはオブジェクトとして扱う
        r_path = resource_path
        self.frame_lb = tk.LabelFrame(root, text=u"path")
        self.button_open = tk.Button(self, text=u"PDFを開く", command=self.open)
        self.button_exit = tk.Button(self, text=u"終了", command=self.exit)
        self.button_append = tk.Button(self, text=u"結合して保存", command=self.append, width=12)
        self.button_split = tk.Button(self, text=u"分割して保存", command=self.split, width=12)
        self.button_clear = tk.Button(self, text=u"クリア", command=self.clear, width=12)
        self.button_up = tk.Button(self, text=u"上移動", command=self.up)
        self.button_down = tk.Button(self, text=u"下移動", command=self.down)
        self.button_number = tk.Button(self, text=u"図面工番全読込", command=self.numscan)
        self.dolphine = tk.PhotoImage(file="dol.png")
        self.canvas = tk.Canvas(bg="gray", width=50, height=50)
        self.canvas.bind("<Button-1>", self.allscan)


    # リストボックス作成
    def listbox(self):
        argvs = tk.StringVar(value=FILE_LIST)
        self.listbox = tk.Listbox(self.frame_lb, listvariable=argvs, width=43, height=7, relief=tk.RIDGE, bd=2)
        self.scrollbar = tk.Scrollbar(self.frame_lb, orient="v", command=self.listbox.yview)
        self.listbox['yscrollcommand'] = self.scrollbar.set
        self.listbox.grid(row=0, column=0)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.listbox.bind("<Button-3>", self.one_clear)

    # 場所
    def place(self):
        self.frame_lb.place(x=7, y=1)
        self.button_open.place(x=300, y=170)
        self.button_exit.place(x=360, y=170)
        self.button_append.place(x=300, y=38)
        self.button_split.place(x=300, y=65)
        self.button_clear.place(x=300, y=140)
        self.button_up.place(x=300, y=10)
        self.button_down.place(x=348, y=10)
        self.button_number.place(x=60, y=140)
        self.canvas.place(x=7, y=140)
        self.canvas.create_image(0, 0, image=self.dolphine, anchor=tk.NW)

    # コマンド
    def open(self):
        global FILE_LIST
        file = tkFD.askopenfilenames(filetypes=[("pdf files", "*.pdf")],initialdir=os.getcwd())
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
    def append(self):
        if bool(FILE_LIST) == False:
            tkMB.showinfo("警告!", "ファイルを開いてください。")
        else:
            merger = PdfFileMerger()
            for fl in FILE_LIST:
                merger.append(fl)

            file = tkFD.asksaveasfilename(filetypes=[("pdf files", "*.pdf")],initialdir=os.path.join(os.getcwd(), "/append/"))
            if not file:
                return

            merger.write(file)
            merger.close()
            tkMB.showinfo("", "結合完了")

    # ぶんかつ保存
    def split(self):
        sub_win = tk.Toplevel(master=self.master)
        sub_win.resizable(width=False, height=False)
        sub_win.title(u"分割設定")
        sub_win.geometry("150x100+100+100")

        def button1_clk():
            print("test")

        f1 = button1_clk

        self.frame_lb = tk.LabelFrame(sub_win, text=u"ページ番号指定")
        self.checkbox = tk.Checkbutton(self.frame_lb, text=u"両方保存する")
        self.button = tk.Button(sub_win, text=u"実行", width=18)
        self.frame_lb.place(x=7, y=1)
        self.checkbox.grid(row=1, column=0)
        self.button.place(x=7, y=67)

        argvs = tk.StringVar()
        self.spinbox = tk.Spinbox(self.frame_lb, textvariable=argvs, from_=0, to=200)
        self.spinbox.grid(row=0, column=0)

        sub_win.transient(self.master)
        sub_win.grab_set()

    # クリア
    def clear(self):
        global FILE_LIST
        for i in range(len(FILE_LIST)):
            self.listbox.delete(i, tk.END)
        FILE_LIST.clear()

    # ひとつだけクリア
    def one_clear(self, ls):
        global FILE_LIST
        for i in self.listbox.curselection():
            self.listbox.delete(i)
            del FILE_LIST[i]

    # 上にあがる
    def up(self):
        global FILE_LIST
        add_list = list(FILE_LIST)
        for i in range(len(add_list)):
            sp = os.path.basename(add_list[i])
            add_list[i] = sp
        for i in self.listbox.curselection():
            if i == 0:
                tkMB.showinfo("エラー", "上移動できません。")
                break
            else:
                add_list[i], add_list[i-1] = add_list[i-1], add_list[i]
                FILE_LIST[i], FILE_LIST[i-1] = FILE_LIST[i-1], FILE_LIST[i]
                self.listbox.delete(i)
                self.listbox.insert(i-1, add_list[i-1])

    # 下にさがる
    def down(self):
        global FILE_LIST
        add_list = list(FILE_LIST)
        for i in range(len(add_list)):
            sp = os.path.basename(add_list[i])
            add_list[i] = sp
        for i in self.listbox.curselection():
            if i == FILE_LIST.index(FILE_LIST[-1]):
                tkMB.showinfo("エラー", "下移動できません")
                break
            else:
                add_list[i], add_list[i+1] = add_list[i+1], add_list[i]
                FILE_LIST[i], FILE_LIST[i+1] = FILE_LIST[i+1], FILE_LIST[i]
                self.listbox.delete(i)
                self.listbox.insert(i+1, add_list[i+1])

    # フルスキャン
    def allscan(self, args):
        global FILE_LIST
        if self.listbox.curselection() == False:
            return
        for i in self.listbox.curselection():
            rsrcmgr = PDFResourceManager()
            rettxt = StringIO()
            laparams = LAParams()
            laparams.detect_vertical = True
            device = TextConverter(rsrcmgr, rettxt, codec='utf-8', laparams=laparams)
            fp = open(FILE_LIST[i], 'rb')
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            for page in PDFPage.get_pages(fp, pagenos=None, maxpages=0, password=None,caching=True, check_extractable=True):
                interpreter.process_page(page)

            search = rettxt.getvalue()

            fp.close()
            device.close()
            rettxt.close()

    def numscan(self):
        if self.listbox.curselection() == False:
            return

        for i in self.listbox.curselection():
            path = FILE_LIST[i]
            images = convert_from_path(path)
            j = 0
            for image in images:
                image.save("test{}.png".format(i), "png")
                i += 1


    
if __name__ == '__main__':
    app = Application(master=root)
    app.pack()
    app.mainloop()
