import customtkinter
import main
import tkinter as tk

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



class App(customtkinter.CTk):
    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("Simulation launcher")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.list_contact_frame = customtkinter.CTkFrame(master=self)
        self.list_contact_frame.grid(column=0, row=0, sticky="nswe", padx=20, pady=20)

        self.right_frame = customtkinter.CTkFrame(master=self)
        self.right_frame.grid(column=1, row=0, sticky='nswe', padx=20, pady=20)

        self.contact_listBox = tk.Listbox(master=self.list_contact_frame)
        self.contact_listBox.grid(column=0, row=0)

        self.mainloop()



app=App()