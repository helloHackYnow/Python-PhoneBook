import zipfile
import csv

def read(path:str) -> list:
    """
    Charge un fichier csv et le met dans une liste de dictionnaires (de clés identiques)
    """
    with open(path, newline='') as csvfile:
        annuaire_dictReader = csv.DictReader(csvfile)
        annuaire_list = []
        for row in annuaire_dictReader:
            annuaire_list.append(row)
        csvfile.close()
        return(annuaire_list)

def write(path:str, annuaire_list:list):
    """
    Récupère liste de dictionnaires (de clés identiques) et l'enregistre dans un fichier csv
    """
    with open(path, 'w', newline='') as csvfile:
        fieldnames = ['nom', 'numero', 'photo_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for contact in annuaire_list:
            writer.writerow(contact)
        csvfile.close()

print(read('contact_list.csv'))
