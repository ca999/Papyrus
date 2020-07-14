from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import tkinter.scrolledtext as scrolledtext


class TextEditor:
    clippy = dict()

    def __init__(self, root):

        self.root = root
        self.root.title("Papyrus")
        self.root.geometry("1200x700+200+150")
        self.filename = None
        self.title = StringVar()
        self.status = StringVar()
        self.titlebar = Label(self.root, textvariable=self.title, font=("times new roman", 15, "bold"), bd=2,
                              relief=GROOVE)
        self.titlebar.pack(side=TOP, fill=BOTH)
        self.settitle()

        self.statusbar = Label(self.root, textvariable=self.status, font=("times new roman", 15, "bold"), bd=2,
                               relief=GROOVE)
        self.statusbar.pack(side=BOTTOM, fill=BOTH)
        self.status.set("Papyrus")

        self.menubar = Menu(self.root, font=("times new roman", 15, "bold"), activebackground="skyblue")
        self.root.config(menu=self.menubar)

        self.filemenu = Menu(self.menubar, font=("times new roman", 12, "bold"), activebackground="skyblue", tearoff=0)
        self.filemenu.add_command(label="New", accelerator="Ctrl+N", command=self.newfile)

        self.filemenu.add_command(label="Open", accelerator="Ctrl+O", command=self.openfile)

        self.filemenu.add_command(label="Save", accelerator="Ctrl+S", command=self.savefile)

        self.filemenu.add_command(label="Save As", accelerator="Ctrl+A", command=self.saveasfile)

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Exit", accelerator="Ctrl+E", command=self.exit)

        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.editmenu = Menu(self.menubar, font=("times new roman", 12, "bold"), activebackground="skyblue", tearoff=0)
        self.editmenu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut)
        self.editmenu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy)
        self.editmenu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste)
        self.editmenu.add_command(label="Undo", accelerator="Ctrl+U", command=self.undo)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        self.helpmenu = Menu(self.menubar, font=("times new roman", 12, "bold"), activebackground="skyblue", tearoff=0)
        self.helpmenu.add_command(label="About", command=self.infoabout)

        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.txt = scrolledtext.ScrolledText(self.root, undo=True)
        self.txt['font'] = ('consolas', '12')
        self.txt.pack(side=LEFT, fill='both')

        self.pastecanvas = Canvas(self.root, bg="white")
        self.pastecanvas.pack(side=RIGHT, expand="True", fill="both")
        self.pastescroll = Scrollbar(self.pastecanvas, orient=VERTICAL)

        self.pastecanvas.config(yscrollcommand=self.pastescroll.set)
        self.pastescroll.pack(side=RIGHT, fill=Y)
        self.shortcuts()
        self.infoabout()

    def settitle(self):

        if self.filename:
            self.title.set(self.filename)
        else:
            self.title.set("Unscroll")

    def newfile(self, *args):

        self.txt.delete("1.0", END)
        self.filename = None
        self.settitle()
        self.status.set("New Scroll Created")

    def openfile(self, *args):

        try:
            self.filename = filedialog.askopenfilename(title="Select file", filetypes=(
                ("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py")))

            if self.filename:

                infile = open(self.filename, "r")
                self.txt.delete("1.0", END)

                for line in infile:
                    self.txt.insert(END, line)

                infile.close()
                self.settitle()
                self.status.set("Unscrolled successfully")

        except Exception as e:
            messagebox.showerror("Exception", e)

    def savefile(self, *args):
        try:

            if self.filename:
                data = self.txt.get("1.0", END)
                outfile = open(self.filename, "w")
                outfile.write(data)
                outfile.close()
                self.settitle()
                self.status.set("Engrained")

            else:
                self.saveasfile()
        except Exception as e:
            messagebox.showerror("Exception", e)

    def saveasfile(self, *args):

        try:
            untitledfile = filedialog.asksaveasfilename(title="Save file As", defaultextension=".txt",
                                                        initialfile="Untitled.txt", filetypes=(
                    ("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py")))

            data = self.txt.get("1.0", END)
            outfile = open(untitledfile, "w")
            outfile.write(data)
            outfile.close()

            self.filename = untitledfile
            self.settitle()
            self.status.set("Saved Successfully")

        except Exception as e:
            messagebox.showerror("Exception", e)

    def exit(self, *args):
        op = messagebox.askyesno("WARNING", "Your Unsaved Data May be Lost!!")

        if op > 0:
            self.root.destroy()
        else:
            return

    def cut(self, *args):
        self.txt.event_generate("<<cut>>")

    def copy(self, *args):
        self.txt.clipboard_clear()
        self.txt.clipboard_append(string=self.txt.selection_get())

    def copytoclip(self, t):
        #messagebox.showinfo("umm yej")
        self.txt.clipboard_clear()
        self.txt.clipboard_append(string=t)

    def buttondestroy(self, t):
        self.clippy[t].destroy()
        del self.clippy[t]

    def paste(self, *args):
        clippt = self.txt.clipboard_get()
        if clippt not in self.clippy:
            bt = (Button(self.pastecanvas, text=self.txt.clipboard_get()))
            bt.pack(side=TOP, fill="both")
            self.clippy[clippt] = bt
            bt.bind("<Double-Button-1>", lambda event: self.buttondestroy(clippt))
            bt.bind("<Button-1>", lambda event: self.copytoclip(clippt))

    def undo(self, *args):
        try:
            if self.filename:
                self.txt.delete("1.0", END)
                infile = open(self.filename, "r")
                for line in infile:
                    self.txt.insert(END, line)
                infile.close()
                self.settitle()
                self.status.set("Undo")
            else:

                self.txt.delete("1.0", END)
                self.filename = None
                self.settitle()
                self.status.set("Undo")
        except Exception as e:
            messagebox.showerror("Exception", e)

    def infoabout(self):
        messagebox.showinfo("Welcome","Welcome! Papyrus is a simple notepad which makes copying and pasting easier than it already is.\nWhatever you paste into papyrus, is available immediately in the papyrus canvas\nTo copy from the canvas click on the text in the canvas\nTo remove from the canvas double-click on the text.\n ")

    def shortcuts(self):
        self.txt.bind("<Control-n>", self.newfile)
        self.txt.bind("<Control-o>", self.openfile)
        self.txt.bind("<Control-s>", self.savefile)
        self.txt.bind("<Control-a>", self.saveasfile)
        self.txt.bind("<Control-e>", self.exit)
        self.txt.bind("<Control-x>", self.cut)
        self.txt.bind("<Control-c>", self.copy)
        self.txt.bind("<Control-v>", self.paste)
        self.txt.bind("<Control-z>", self.undo)


root = Tk()
p1 = PhotoImage(file = 'icon.png')
root.tk.call('wm', 'iconphoto', root._w, p1)
TextEditor(root)

root.mainloop()
