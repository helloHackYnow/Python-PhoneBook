import use_csv
from tkinter import filedialog as fd
import re


def searchContactsByName(name:str, list_contact):
    name_patern = re.compile(name.lower())
    contacts = []
    print(contacts)
    for i in range(len(list_contact)):
        if name_patern.search(list_contact[i]['nom'].lower()):
            contacts.append(i)
    return contacts

def searchContactByNumero(numero, list_contact):
    contacts = [contact for contact in list_contact if contact['numero']==numero][0]
    return contacts


def ajouterContact(list_contact:list, nom, numero):
    contact={'nom':nom, 'numero':numero}
    list_contact.append(contact)

def supprimerContact(list_contact, nom=None, numero=None):
    contact = None
    if nom != None:
        contact = [contact for contact in list_contact if contact['nom']==nom][0]
    elif numero!=None:
        contact = [contact for contact in list_contact if contact['numero']==numero][0]
    
def verifierContact(list_contact, nom=None, numero=None):
    pass

def verifierNumero(numero:str):
    if len(numero.replace(' ', ''))==10:
        output = numero.replace(' ', '')
        try:
            int(numero)
        except:
            output=False
    else:
        output = False
    return(output)


def printContact(contact):
    print(f"{contact['nom']}: {contact['numero']}")

def saveChanges(path, contact_list):
    use_csv.write(path, contact_list)

