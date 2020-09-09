from experiment_server_GUI import Experiment_Server_GUI
from tkinter import *
from utils import *

run_local = False

root = Tk()

app = Experiment_Server_GUI(root=root, run_local=run_local)

def on_closing():
    app.close_server()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()