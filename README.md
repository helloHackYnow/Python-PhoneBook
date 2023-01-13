# Project Annuaire

This is a project I made for school.  
The interface is made with [customTkinter](https://github.com/TomSchimansky/CustomTkinter).
There is still a lot of bugs or unusable features, but I will improve the project if it's needed.

## File format
To save the phonebook, I created file format .annuaire ( annuaire = phonebook in french ).
In fact, it's just .zip archive renamed, wich contain :
1.  A list_contact.csv file, which contain all the informations of the contacts
1.  Pictures of the contacts  

I'm sure thinking this is not an optimal solution, so feel free to make suggestions !

## Installation
I don't tkink this project is the kind of project to be PyPi, but you can still clone the repo ✅  
There is the code to install the requierments :
```
cd path/of/the/repos
pip install requirements.txt
```

## Usage 

To start the program, run gui.py

## Settings

The gui.py script contain parameters you can easily change to modifie the behaviour of the application :  
1. ``OPEN_NEW_ANNUAIRE_AT_LAUNCH = True``  
    As you might, it define if the program ask you to select an annaire file to open at launch.  
    If set on ``False``, the program will automatically load the empty.annuaire file locate in the ``default_templates`` folder.
2. ``TMP_DIR = "tmp"``  
    To handle the .annuaire files, the program need a folder to store temporary files.  
    This parameter define the path of this folder.
3. ``DEFAULT_TEMPLATE_PATH = "default_templates/empty.annuaire"``  
    This define the path of the "copy" icon.  
    You change it to change this icon 🤷‍♂️ ( or the directorie where the icon is store )  
4. ``SAVE_AS_AT_EXIT = False``  
    Set if the program automaticaly ask you to save as your .annuaire file on closing the application
