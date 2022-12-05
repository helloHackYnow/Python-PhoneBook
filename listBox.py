import customtkinter
from typing import Union, Callable
import tkinter


class ListBox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 200,
                 height: int = 400,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.command = command
    

app = customtkinter.CTk()

spinbox_1 = ListBox()


app.mainloop()