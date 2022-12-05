import customtkinter
import main
import tkinter as tk
import use_csv

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



class App(customtkinter.CTk):
    WIDTH = 780
    HEIGHT = 520
    MAX_CONTACT_PER_PAGE = 11

    def __init__(self):
        super().__init__()

        self.contact_list = []
        
        self.title("Simulation launcher")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.right_frame = customtkinter.CTkFrame(master=self)
        self.right_frame.grid(column=1,columnspan=2, row=0, sticky='nswe', padx=20, pady=20)

        self.contact_list = use_csv.read('annuaire.csv')
        self.create_contact_tab()

        self.mainloop()

    def create_contact_tab(self):
        #Contact tab view
        self.list_contact_tab = customtkinter.CTkTabview(master=self, width=10)
        self.list_contact_tab.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.list_button_contact = [customtkinter.CTkButton]

        nb_contact = len(self.contact_list)
        nb_pages = nb_contact // App.MAX_CONTACT_PER_PAGE
        if nb_contact % App.MAX_CONTACT_PER_PAGE != 0:
            nb_pages += 1
        for i in range(0, nb_pages):
            self.list_contact_tab.add(f"Page {i+1}")
            self.list_contact_tab.tab(f"Page {i+1}").grid_columnconfigure(0, weight=1)

        for contact_index in range(nb_contact):
            page_index = (contact_index // App.MAX_CONTACT_PER_PAGE)+1
            contact_name = self.contact_list[contact_index].get('nom')
            print(contact_name)
            
            button = customtkinter.CTkButton(master=self.list_contact_tab.tab(f"Page {page_index}"), text=contact_name)
            button.grid(row=contact_index, columnspan=2, pady=5, padx=5, sticky="s")
            self.list_button_contact.append(button)
        self.update()

        

        



app=App()
