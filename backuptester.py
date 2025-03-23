from async_tkinter_loop import async_mainloop, async_handler
from tkinter import *
from tkinter import Tk, ttk
from tkinter.font import Font
import asyncio
from datetime import datetime
from pathlib import Path

TITLE = ""
WIDTH = 800
HEIGHT = 570
RESIZABLE = False, False
MYSQL_BIN_PATH = r"C:\Program Files\MySQL\MySQL Server 8.3\bin"

running = False

class App():

    @staticmethod
    def _find_center(root: Tk, W: int, H: int) -> str:
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        # Compute for x and y coordinates
        x_pos = int((screenwidth-W)/2)-10
        y_pos = int((screenheight-H)/2)-20
        return "{0}x{1}+{2}+{3}" \
            .format(W, H, x_pos, y_pos)
    
    async def _restore_db(self, host, user, password, port, filepath):
        cmd = None

        cmd = f'"{MYSQL_BIN_PATH}\\mysql.exe" '
        cmd += "--host={} ".format(host)
        cmd += "--user={} ".format(user)
        cmd += "--password={} ".format(password)
        cmd += "--port={} ".format(port)
        cmd += '--execute="SELEC1"'
        # cmd += "< {}".format(filepath)

        print(cmd)
        
        proc = await asyncio.create_subprocess_shell(cmd,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE)
        
        stdout, stderr = await proc.communicate()

        # print("return code", proc.returncode)
        # print("stderr", stderr.decode())
        # print("stdout", stdout.decode())
        
        if proc.returncode is not None \
            and proc.returncode == 1:
            print("Err ", stderr.decode())
        if (proc.returncode and proc.returncode == 0) \
                or (proc.returncode and proc.returncode != 1):
            print("Output ", stdout.decode())

    async def _missing_tables_check():
        pass

    async def _missing_data_check():
        pass

    
    @async_handler
    async def _test_restore(self):
        global running 
        running = True
        self.StopTestBtn.configure(state="normal")
        self.StartTestBtn.configure(state="disabled")
        self.Notebook.select(1)
        logs = ["Started test restore.\n",
                "Connecting to the source server.\n",
                "Executing 'C:\Program Files\MySQL\MySQL Server 8.3\bin\mysql.exe --host=localhost --user=root --password=********* --database backupdb < .\dumps.sql'.\n",
                "Test restore was successful. Duration 10.5423 seconds.\n"]
        
        for i in range(20):
            for lognum in range(len(logs)):
                if running:
                    if lognum == 3:
                        await asyncio.sleep(5)
                        self.Text.insert(END,
                                f"{datetime.now()} {logs[lognum]}")
                    else:
                        self.Text.insert(END,
                            f"{datetime.now()} {logs[lognum]}")
                    await asyncio.sleep(0.1)
                else:
                    self.StopTestBtn.configure(state="disabled")
                    self.StartTestBtn.configure(state="normal")
                    break

        self.StopTestBtn.configure(state="disabled")
        self.StartTestBtn.configure(state="normal")
        
    def _stop_test(self):
        global running
        if running:
            self.StopTestBtn.configure(state="disabled")
            self.StartTestBtn.configure(state="normal")
            running = False
            self.Text.insert(END,
                f"{datetime.now()}, Stopped.\n")

    def __init__(self) -> None:
        self.Root = Tk()
        self.Root.geometry(self._find_center(self.Root, WIDTH, HEIGHT))
        # self.Root.resizable(*RESIZABLE)

        # Checks for any active installation of mysql server
        import subprocess
        cmd = "where mysql.exe"
        proc = subprocess.run(cmd, check=False,
            capture_output=True, shell=True)
        if proc.stderr:
            print(proc.stderr)
            return

        self.MainFrame = Frame(self.Root)
        self.MainFrame.pack(fill=BOTH, expand=TRUE)


        self.TopFrame = Frame(self.MainFrame)
        self.MiddleFrame = Frame(self.MainFrame)
        self.BottomFrame = Frame(self.MainFrame)

        # Widgets
        self.Notebook = ttk.Notebook(self.MiddleFrame,)
        self.Notebook.pack()
        self.TabFrame1 = Frame(self.MiddleFrame, background="white", padx=10)
        self.TabFrame2 = Frame(self.MiddleFrame, background="white", padx=10)
        self.Notebook.add(self.TabFrame1, text="Configure Test Server")
        self.Notebook.add(self.TabFrame2, text="Restore Progress")

        self.NewFont = Font(family="Calibri (Body)", weight="normal", size=14)
        self.TextFont = Font(family="Calibri (Body)", weight="normal", size=8)

        self.Label1 = Label(self.TopFrame, text="MySQL ver 5.5", font=self.NewFont).pack(anchor=W)

        self.Notebook.pack(expand=TRUE, fill=BOTH)
        
        self.TopFrame.pack(fill=X, side=TOP, padx=10, pady=10)
        self.MiddleFrame.pack(side=TOP, fill=BOTH, padx=10, pady=10)
        self.BottomFrame.pack(fill=BOTH, side=BOTTOM, padx=10, pady=10)


        self.TabFrame2_Tab1 = Frame(self.TabFrame2, background="white")
        self.TabFrame2_Tab2 = Frame(self.TabFrame2, background="white")
        self.TabFrame2_Tab1.pack(side=TOP, fill=X)
        self.TabFrame2_Tab2.pack(side=TOP, fill=BOTH, expand=TRUE)

        self.Label = Label(self.TabFrame2_Tab1, text="Log:", background="white").pack(anchor=W)
        self.Label = Label(self.TabFrame2_Tab1, text="Log:", background="white").pack(anchor=W)
        self.Label = Label(self.TabFrame2_Tab1, text="Log:", background="white").pack(anchor=W)
        self.Label = Label(self.TabFrame2_Tab1, text="Log:", background="white").pack(anchor=W)

        self.YScrollBar = Scrollbar(self.TabFrame2_Tab2, orient="vertical")
        self.Text = Text(self.TabFrame2_Tab2, font=self.TextFont, yscrollcommand=self.YScrollBar.set)
        self.YScrollBar.configure(command=self.Text.yview)
        self.YScrollBar.pack(side=RIGHT, fill=Y)
        self.Text.pack(fill=BOTH, expand=True)

        # for i in range(100):
        #     self.Text.insert(END, 
        #         f"{datetime.now()} Test logs {i}\n")
        
        

        self.StartTestBtn = ttk.Button(self.BottomFrame, text="Start Test", command=lambda: self._test_restore())
        self.StopTestBtn = ttk.Button(self.BottomFrame, text="Stop", state="disabled", command=lambda: self._stop_test())
        self.StartTestBtn.pack(side=RIGHT, padx=5)
        self.StopTestBtn.pack(side=RIGHT, padx=5)

        # Pack widgets 

        # Keyboard binds
        self.Root.bind("<Escape>",
            lambda e: self.Root.destroy())

        # Run app
        # self.Root.mainloop()
        async_mainloop(self.Root)



if __name__ == "__main__":
    
    app = App
    app()