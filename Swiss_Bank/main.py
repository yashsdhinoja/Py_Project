import tkinter as tk
from tkinter import simpledialog # Pre-load sub-module for dialog inputs
from gui_app import SwissBankApp

if __name__ == "__main__":
    root = tk.Tk()
    # Attach simpledialog to tk namespace for seamless dialog pops
    tk.simpledialog = simpledialog
    app = SwissBankApp(root)
    root.mainloop()

    
    # Cyra@00004
    # Qwerty&00007