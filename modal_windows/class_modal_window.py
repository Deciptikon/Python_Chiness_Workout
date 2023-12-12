import tkinter as tk

class ModalWindow(object):
    modal_window = None
    
    def __init__(self, 
                 root, 
                 name_window: str = "Name Window", 
                 geometry: str = '400x300+600+200') -> None:
        self.root = root
        self.modal_window = tk.Toplevel(self.root)
        self.modal_window.title(name_window)
        self.modal_window.geometry(geometry)
        
        
        