import use_csv
from tkinter import filedialog as fd
from copy import deepcopy

def trouverContact(list_contact, nom=None, numero=None):
    contact = None
    if nom != None:
        contact = [contact for contact in list_contact if contact['nom']==nom][0]
    else:
        contact = [contact for contact in list_contact if contact['numero']==numero][0]
    return(contact)

def ajouterContact(list_contact, nom, numero):
    pass

def supprimerContact(list_contact, nom=None, numero=None):
    pass

def verifierNumero(numero:str):
    if len(numero.replace(' ', ''))==10:
        output = numero.replace(' ', '')
    else:
        output = False


def printContact(contact):
    print(f"{contact['nom']}: {contact['numero']}")

def saveChanges(path, contact_list):
    use_csv.write(path, contact_list)

def menu():
    print("Bienvenue dans votre annuaire !")
    path_dico = fd.askopenfilename(title="Ouvrez votre annuaire", filetypes=[("csv file", "*.csv")], initialdir='/')
    annuaire = deepcopy(use_csv.read(path_dico))

    while 1:
        print("Veuillez choisir une des options suivantes :")
        print("     1- Trouver un contact")
        print("     2- Ajouter un contact")
        print("     3- Supprimer un contact")
        print("     4- Sauvegarder les changements")
        print("     5- Sortir de l'application")
        choix = int(input("Votre choix: "))
        match choix:
            case 1:
                print("     1- Trouver le contact à partir du numero")
                print("     2- Trouver le contact à partir du nom")
                choix = int(input("Votre choix: "))
                match choix:
                    case 1:
                        numero = verifierNumero(input("Numéro: "))
                        contact = trouverContact(annuaire, numero=numero)                   
                    case 2:
                        nom = input("Nom: ")
                        contact = trouverContact(annuaire, nom=nom)
                        printContact(contact)
            case 2:
                ajouterContact()
            case 3:
                supprimerContact()
            case 4:
                path = fd.asksaveasfilename(title="Ouvrez votre annuaire", filetypes=[("csv file", "*.csv")], initialdir='/')
                saveChanges(path, annuaire)
            case 5:
                break
            case _:
                print("Veuillez renter un choix valide")

menu()

