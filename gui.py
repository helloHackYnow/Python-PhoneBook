from tkinter import filedialog
import customtkinter
import annuaire
import tkinter as tk
import use_csv
import pyperclip
from PIL import ImageTk, Image
import shutil
import os
import glob

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    WIDTH = 780
    HEIGHT = 550
    MAX_CONTACT_PER_PAGE = 11 #Nombre de contact par page de la liste de contact
    NB_RESULT_WIDHT = 4 #Largeur de la grille de resultat
    NB_RESULT_HEIGHT = 3 #Hauteur de la grille de resultat
    OPEN_NEW_ANNUAIRE_AT_LAUNCH = True 
    TMP_DIR = "tmp" #Chemin d'accès du dossier 
    DEFAULT_TEMPLATE_PATH = "default_templates/empty.annuaire"
    
    def __init__(self):
        super().__init__()

        self.contact_list = []
        
        self.title("Annuaire")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.right_frame = customtkinter.CTkFrame(master=self)
        self.right_frame.grid(column=1,columnspan=2, row=0, sticky='nswe', padx=20, pady=20, rowspan=2)

        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure((0, 1), weight=1)

        self.search_interface_frame = customtkinter.CTkFrame(master=self.right_frame)
        self.search_interface_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")

        self.search_interface_frame.grid_columnconfigure(1, weight=1)

        self.result_interface_frame = customtkinter.CTkFrame(master=self.right_frame)
        self.result_interface_frame.grid(row=1, column=0, padx=20, pady=(10, 20), sticky='nsew')

        self.result_interface_frame.grid_columnconfigure(0, weight=1)
        self.result_interface_frame.grid_rowconfigure(0, weight=1)
        
        self.is_modification_window_open = False

        if App.OPEN_NEW_ANNUAIRE_AT_LAUNCH:
            path = filedialog.askopenfilename(filetypes=[('Annuaire file', '*.annuaire')])
            self.unpackFile(path)
        
        else:
            path = App.DEFAULT_TEMPLATE_PATH
            self.unpackFile(path)
            
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.mainloop()

    def on_closing(self):
        self.saveFile()
        self.destroy()
    
    def create_contact_tab(self):
        """
        Create the tab view on the left that serve to display a list of the contacts
        """
        #Contact tab view
        self.list_contact_tab = customtkinter.CTkTabview(master=self, width=10)
        self.list_contact_tab.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.list_button_contact = [customtkinter.CTkButton]

        nb_contact = len(self.contact_list)
        nb_pages = nb_contact // App.MAX_CONTACT_PER_PAGE

        #Create each tab one by one
        if nb_contact % App.MAX_CONTACT_PER_PAGE != 0:
            nb_pages += 1
            
        for i in range(0, nb_pages):
            self.list_contact_tab.add(f"Page {i+1}")
            self.list_contact_tab.tab(f"Page {i+1}").grid_columnconfigure(0, weight=1)

        #Create each button one by one
        for contact_index in range(nb_contact):
            page_index = (contact_index // App.MAX_CONTACT_PER_PAGE)+1
            contact_name = self.contact_list[contact_index].get('nom')
            print(contact_name)
            
            button = customtkinter.CTkButton(master=self.list_contact_tab.tab(f"Page {page_index}"), text=contact_name, 
                                            command=lambda x=contact_index:self.create_contact_modification_window(contact_index=x))
            button.grid(row=contact_index, columnspan=2, pady=5, padx=5, sticky="s")
            self.list_button_contact.append(button)

        #Create the 'add' button
        self.add_button = customtkinter.CTkButton(master=self, text="Add", command=self.addContactButton)
        self.add_button.grid(row=1, column=0, sticky="eswn", padx=(25, 0), pady=(0, 20))
        self.update()

    def createSearchInterface(self):
        """
        Create the search interface for the application. This includes a label, two entry fields for searching by name or number, and a button to initiate the search.
        """
        self.searchLabel = customtkinter.CTkLabel(master=self.search_interface_frame, text="Search", font=customtkinter.CTkFont(size=45, weight="bold"))
        self.searchLabel.grid(row=0, column=0, padx=30, pady=20)

        self.search_by_name_entry = customtkinter.CTkEntry(master=self.search_interface_frame, placeholder_text='Search by name')
        self.search_by_name_entry.grid(row=1, column=0, padx=(30, 10), pady=20, sticky='w')

        self.search_by_numero_entry = customtkinter.CTkEntry(master=self.search_interface_frame, placeholder_text='Search by numero')
        self.search_by_numero_entry.grid(row=2, column=0, padx=(30, 10), pady=(20, 40), sticky='w')
        self.search_button = customtkinter.CTkButton(master=self.search_interface_frame, text='Search', command=self.searchButtonFunc)
        self.search_button.grid(row=2, column=1, sticky='e', padx=30, pady=(20, 40))
        self.update()

    def createResultInterface(self):
        """
        Create the tab wich display the result of search
        """

        self.result_tab = customtkinter.CTkTabview(master=self.result_interface_frame, height=170)
        self.result_tab.grid(row=0, column=0, sticky='nwse', padx=20, pady=20)

        nb_contact_per_pages = App.NB_RESULT_WIDHT*App.NB_RESULT_HEIGHT
        nb_contact = len(self.list_contacts_result)
        nb_pages = nb_contact // nb_contact_per_pages

        self.list_buttons_result = []

        if nb_contact % nb_contact_per_pages != 0:
            nb_pages += 1
        for i in range(0, nb_pages):
            self.result_tab.add(f"{i+1}")
            for x in range(0, App.NB_RESULT_WIDHT+1):
                self.result_tab.tab(f"{i+1}").grid_columnconfigure(x, weight=1)
            for y in range(0, App.NB_RESULT_HEIGHT+1):
                self.result_tab.tab(f"{i+1}").grid_columnconfigure(y, weight=1)
        index_in_tab_result = 0

        for contact_result_index in self.list_contacts_result:
            print(contact_result_index)
            tab_index = index_in_tab_result // nb_contact_per_pages + 1
            x_index = index_in_tab_result % App.NB_RESULT_WIDHT
            y_index = index_in_tab_result // App.NB_RESULT_WIDHT

            contact_button = customtkinter.CTkButton(master=self.result_tab.tab(f"{tab_index}"), text=self.contact_list[contact_result_index]['nom'],
                                                            command=lambda x=contact_result_index:self.create_contact_modification_window(contact_index=x))
            contact_button.grid(row=y_index, column=x_index, padx=5, pady=5)
            self.list_buttons_result.append(contact_button)
            
            index_in_tab_result+=1
        self.update()
    
    def create_contact_modification_window(self, contact_index):
        """
        Create a pop-up window wich can modifie or delete a contact
        """
        if not self.is_modification_window_open:
            self.is_modification_window_open = True
            self.current_contact_index = contact_index

            name:str = self.contact_list[contact_index].get('nom')
            numero = self.contact_list[contact_index].get('numero')
            img = None
            if self.contact_list[contact_index].get('photo_name') != 'None':
                photo_path = f'{App.TMP_DIR}/'+self.contact_list[contact_index].get('photo_name')
                img = customtkinter.CTkImage(Image.open(photo_path),
                                                size=(200, 200))
                

            self.contact_modification_window = customtkinter.CTkToplevel()
            self.contact_modification_window.title(f"Modifier le contact {name}")
            self.contact_modification_window.geometry("730x230")

            self.contact_modification_window.protocol("WM_DELETE_WINDOW", self.onModificationWindowClose)

            self.contact_modification_window.grid_columnconfigure(1, weight=1)

            self.contact_modification_window.grid_rowconfigure(0, weight=0)
            self.contact_modification_window.grid_rowconfigure(1, weight=1)

            self.left_frame_subWindow = customtkinter.CTkFrame(master=self.contact_modification_window, corner_radius=0, width=140)
            self.left_frame_subWindow.grid(row=0, column=0, rowspan=2, padx=0, pady=0, sticky="nswe")
            self.left_frame_subWindow.grid_rowconfigure(0, weight=1)
            self.left_frame_subWindow.grid_rowconfigure(1, weight=0)

            self.title_subWindow = customtkinter.CTkLabel(master=self.left_frame_subWindow, text=name.replace(' ', '\n'), font=customtkinter.CTkFont(size=25, weight="bold"))
            self.title_subWindow.grid(padx=20, pady=20, sticky="n")

            self.del_contact_button = customtkinter.CTkButton(master=self.left_frame_subWindow, text="Supprimer", command=self.deleteContact)
            self.del_contact_button.grid(sticky="ews", padx=10, pady=10)
            
            self.right_frame_subWindow = customtkinter.CTkFrame(master=self.contact_modification_window)
            self.right_frame_subWindow.grid(row=0, column=1, rowspan=2, padx=15, pady=15, sticky="nswe")
            self.right_frame_subWindow.grid_columnconfigure((0, 1), weight=1)
            self.right_frame_subWindow.grid_rowconfigure((0, 2), weight=0)
            self.right_frame_subWindow.grid_rowconfigure(1, weight=1)

            self.label_modification = customtkinter.CTkLabel(master=self.right_frame_subWindow, text="Modification", font=customtkinter.CTkFont(size=20, weight="bold"))
            self.label_modification.grid(row=0, column=0, sticky="ws", padx=15, pady=10)

            self.name_current_contact = customtkinter.StringVar()
            self.name_current_contact.set(name)
            self.name_entry_modification = customtkinter.CTkEntry(master=self.right_frame_subWindow, textvariable=self.name_current_contact)
            self.name_entry_modification.grid(row=1, column=0, padx=15, pady=15, sticky='ws')

            self.numero_current_contact = customtkinter.StringVar()
            self.numero_current_contact.set(numero)
            self.name_entry_modification = customtkinter.CTkEntry(master=self.right_frame_subWindow, textvariable=self.numero_current_contact)
            self.name_entry_modification.grid(row=2, column=0, padx=15, pady=15, sticky='wn')
            
            self.accept_button_save_changes = customtkinter.CTkButton(self.right_frame_subWindow, text="Save",width=60, command=lambda:self.save_contact_modification())
            self.accept_button_save_changes.grid(row=2, column=1, padx=15, pady=15, sticky='es')

            self.photo_frame = customtkinter.CTkFrame(master=self.contact_modification_window, width=200)
            self.photo_frame.grid(row=0, column=2, padx=15, pady=15)
            if img != None:
                self.photo_label = customtkinter.CTkLabel(self.photo_frame, image=img, text="")
                self.photo_label.grid()
                
            else:
                self.add_img_button = customtkinter.CTkButton(master=self.photo_frame, text="Add Photo", command=self.addImage)
                self.add_img_button.grid(padx=30, pady=87)
            self.contact_modification_window.update()
            self.contact_modification_window.grab_set()

    def onModificationWindowClose(self):
        """
        This focntion is called when the modification window is closed
        """
        self.contact_modification_window.destroy()
        self.redrawInterface()
        self.is_modification_window_open = False

    def verifieChanges(self):
        """
        Verifie if the phone number enter is correct or not
        """
        new_numero = self.numero_current_contact.get()
        new_numero = annuaire.verifierNumero(new_numero)
        if new_numero:
            output=True
        else:
            self.numero_current_contact.set("Please enter a correct number")
            output = False
        return output
            
    def redrawInterface(self):
        """
        Reset the result tab and redraw the inteface
        """
        self.result_tab=None
        self.create_contact_tab()
        self.createSearchInterface()

    def save_contact_modification(self):
        if self.verifieChanges():
            new_name = self.name_current_contact.get()
            print(f"New name : {new_name}")
            new_numero = self.numero_current_contact.get()
            self.contact_list[self.current_contact_index]['nom'] = new_name
            self.contact_list[self.current_contact_index]['numero'] = new_numero

            annuaire.saveChanges(f"{App.TMP_DIR}/contact_list.csv", self.contact_list)
            self.onModificationWindowClose()

    def searchButtonFunc(self):
        """
        This fonction is called when 
        """
        name = self.search_by_name_entry.get()
        numero = self.search_by_numero_entry.get()

        if name != "":
            self.list_contacts_result = annuaire.searchContactsByName(name, self.contact_list)
        elif numero != "":
            self.list_contacts_result = annuaire.searchContactByNumero(numero, self.contact_list)
        else:
            self.list_contacts_result = []
        self.createResultInterface()
        

    def deleteContact(self):
        """
        Remove the currently selected contact from the list of contacts and save the changes to the CSV file.
        """
        self.contact_list.pop(self.current_contact_index)
        annuaire.saveChanges("working_directorie/contact_list.csv", self.contact_list)
        self.onModificationWindowClose()
    
    def addContactButton(self):
        """
        Add a new default contact to the list of contacts and open the contact modification window for the new contact.
        """
        new_contact= {"nom":"default", "numero":"None", "photo_name":"None"}
        self.contact_list.append(new_contact)
        self.create_contact_modification_window(len(self.contact_list)-1)
    
    def addImage(self):
        image_path = filedialog.askopenfilename(title="Selectionez un image")
        save_folder = App.TMP_DIR
        # Open the image using PIL
        image = Image.open(image_path)
        
        # Crop the image to 200x200 pixels
        image.thumbnail(size=(200, 200))
        
        # Create the save folder if it does not exist
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        
        # Get the file name and extension of the image
        file_name, file_extension = os.path.splitext(os.path.basename(image_path))
        save_path = os.path.join(save_folder, file_name + file_extension)
        image.save(save_path)
        image.close()
        
        self.contact_list[self.current_contact_index]['photo_name'] = file_name + file_extension
        
        self.onModificationWindowClose()
        self.create_contact_modification_window(self.current_contact_index)
    
    def saveFile(self):
        output_filename = filedialog.asksaveasfilename(filetypes=[('Annuaire file', '*.annuaire')]).split(".")[0]
        
        #Delete possibly remaining .zip files
        dir = os.listdir(App.TMP_DIR)

        for file in dir:
            if file.endswith(".zip"):
                os.remove(os.path.join(App.TMP_DIR, file))
        
        shutil.make_archive(output_filename, 'zip', App.TMP_DIR)
        os.replace(f"{output_filename}.zip", f"{output_filename}.annuaire")
        
        files = glob.glob(f'{App.TMP_DIR}/*')
        for f in files:
            os.remove(f)
            
    def unpackFile(self, path):
        new_path = shutil.copy(path, App.TMP_DIR)
        new_name = new_path.split(".")[0]+".zip"
        os.rename(new_path, new_name)
        try:
            shutil.unpack_archive(new_name, App.TMP_DIR)
        except:
            pass
        csv_path = f'{App.TMP_DIR}/contact_list.csv'
        self.contact_list = use_csv.read(csv_path)
        self.redrawInterface()
        
        
        

app=App()
