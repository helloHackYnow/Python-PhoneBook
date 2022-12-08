import csv

def read(path:str) -> list:
    """
    Charge un fichier csv et le met dans une liste de dictionnaire
    """
    with open(path, newline='') as csvfile:
        annuaire_dictReader = csv.DictReader(csvfile)
        annuaire_list = []
        for row in annuaire_dictReader:
            annuaire_list.append(row)
        csvfile.close()
        return(annuaire_list)

def write(path:str, annuaire_list:list):
    with open(path, 'w', newline='') as csvfile:
        fieldnames = ['nom', 'numero']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in annuaire_list:
            writer.writerow(row)
        csvfile.close()