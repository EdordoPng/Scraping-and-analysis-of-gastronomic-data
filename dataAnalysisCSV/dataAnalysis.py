import json
import csv
import os
import configparser

# ENG :

# This program creates a json file named : ingr_storage.csv which contains all ingredients of alla recipes with 0 quantity.
# This program creates also a json file named : ingr_storage1.csv, you can modify this file and initilize the storage.
# You need to set them in the ingr_storage1 that will be used in future files

# ITA :

# Questo programma crea un file json denominato : ingr_storage.csv che contiene tutti gli ingredienti di tutte le ricette con quantità 0.
# Questo programma crea anche un file json denominato: ingr_storage1.csv, è possibile modificare questo file e inizializzare l'archiviazione.
# È necessario impostarli in ingr_storage1 che verrà utilizzato nei file futuri


def obtain_folder_informations():
    """Obtain usefoul datas form the dataAnalysis.conf file."""
    config = configparser.ConfigParser()
    # If the conf file isn't been found, then create a new one
    if not os.path.isfile("dataAnalysis.conf"):
        config["FOLDER TO ANALYZE"] = {
            "folder": "cartella_portate",
        }
        config["JSON TO ANALYZE"] = {
            "file": "Cookbook_SingleServing.json",
        }
        with open("dataAnalysis.conf", "w") as configfile:
            config.write(configfile)
            return "cartella_portate", "Cookbook_SingleServing.json"
    # If the conf is found, then take from there files names of the onbe to be skipped
    else:
        config.read("dataAnalysis.conf")
        folder = config["FOLDER TO ANALYZE"]["folder"]
        file = config["JSON TO ANALYZE"]["file"]
        return folder, file


def update_ingr_counter(name: str, ingredient_usage_record, unita_di_misura):
    """Update the usage counter of the ingredient"""
    # Update the counter of the ingredient, cause it has been used in this recipe
    if name not in ingredient_usage_record:
        ingredient_usage_record.setdefault(
            name, {"Contatore uso": 1, "Unità di misura": unita_di_misura}
        )
    else:
        # Adding the usage at the ingredient dict
        ingredient_usage_record[name]["Contatore uso"] += 1

    # Now if wanted, the ingredients could be sorted alphabetically
    sorted_ingredients = dict(sorted(ingredient_usage_record.items()))

    # Update the ingredient usage record with the sorted dictionary
    ingredient_usage_record.clear()
    ingredient_usage_record.update(sorted_ingredients)


def update_quantity_record(ingrediente, ingredient_quantity_record):
    """Update the quantity of the ingredient"""
    nome = ingrediente["Nome"]
    unita_di_misura = ingrediente["Unità di misura"]
    # If the ingredient name isn't inside the dictionary ingredient_quantity_record
    if nome not in ingredient_quantity_record:
        # Update quantity requested by an ingredient
        if ingrediente["Quantità"] == "q.b.":

            # ENG :
            # Ingredients handled this way will be problematic as I would like to be able to enter a quantity
            # equal to s.h. , but when I then open the sheet in excel the ingredient is not added correctly since then
            # I would have a string in a field where an integer goes. So the one with the string as quantity is discarded

            # ITA :
            # Gli ingredienti gestiti in questo modo saranno problematici in quanto vorrei poter mettere una quantità
            # pari a q.b. , ma quando poi apro il foglio su excel l'ingrediente non viene aggiunto correttamente poiché
            # avrei una stringa in un campo dove ci va un intero. Dunque quello con la stringa come quantità viene scartato

            ingredient_quantity_record.setdefault(
                nome, {"Quantita": "q.b.", "Unità di misura": unita_di_misura}
            )
        else:
            # If the ingredient has a quantity different from "q.b."
            # Put the ingredient with a starting quantity 0
            ingredient_quantity_record.setdefault(
                nome, {"Quantita": 0, "Unità di misura": unita_di_misura}
            )
            # Update the quantity, if not done, we lose the quantity of the first ingredient
            # Used float due to problem given from ingredients with a quantity > 0 and < 1
            ingredient_quantity_record[nome]["Quantita"] += float(
                ingrediente["Quantità"]
            )
    else:
        # If the ingredient hasn been added already, check if has the same unit of measure
        if unita_di_misura != ingredient_quantity_record[nome]["Unità di misura"]:
            # Add the ingredient that already has a name, but a different unit of measurement, so it's another ingredient
            # if I don't go to implement the logic for unit conversions
            ingredient_quantity_record.setdefault(
                nome, {"Quantita": 0, "Unità di misura": unita_di_misura}
            )

        # If the ingredient has the same unit of measure of the one inside storage already,
        # then update quantity of the ingredient
        else:
            if ingredient_quantity_record[nome]["Quantita"] == "q.b.":
                # In this case we have to do nothing
                pass
            # If the ingredient is already inside the storage with a quantity of q.b.
            elif ingrediente["Quantità"] == "q.b.":
                ingredient_quantity_record[nome]["Quantita"] == "q.b."
            # If the quantity is a number, then add it to the already existing quantity count
            else:
                # Used float due to problem given from ingredients with a quantity > 0 and < 1
                ingredient_quantity_record[nome]["Quantita"] += float(
                    ingrediente["Quantità"]
                )


def main():
    # Obtain from the conf file the folder name to use
    # We initialyze also the file name variable that contains the name of the json that need to be used
    folder_name, file_name = obtain_folder_informations()

    # Save the script link on the machine that is executing it. We would use this to came back here later
    script_folder = os.getcwd()
    # With this instruction we move to work into the mother folder of this file, because I need to search the folder_name folder
    # that contains all the json files extracted, one for each Portata
    os.chdir("..")
    # Move to work into cartella_portate
    os.chdir(folder_name)

    # Opening the single serving cookbook
    with open(file_name, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    ingredienti = {}
    # Dict used to take trace of the times an ingredeient has been used into the various recipes
    ingredient_usage_record = {}
    # Dict used to take trace of the quantity needed by an ingredeient into the various recipes
    ingredient_quantity_record = {}

    # Iterate along various recipes
    for ricetta in data:
        # Iterate along all ingredients for all recipes
        for ingrediente in ricetta["Ingredienti"]:
            # Extract ingredient datas
            nome = ingrediente["Nome"]
            unita_di_misura = ingrediente["Unità di misura"]

            # Update ingredient counter dict
            update_ingr_counter(nome, ingredient_usage_record, unita_di_misura)

            update_quantity_record(ingrediente, ingredient_quantity_record)

            # If the ingredient isn't inside the list yet
            if nome not in ingredienti:
                # Update ingredients list
                ingredienti.setdefault(
                    nome, {"Quantita": 0, "Unità di misura": unita_di_misura}
                )

    # With this instruction we move to work back in this script folder, because I need to store here the csv file
    os.chdir("..")
    # Move to work into this script folder. Becouse decided to store the csv file created here into the same of this script folder
    os.chdir(script_folder)

    # -----------------------  Start CSV output creation  -----------------------------

    # --------------------------------------------------------------------------------------------------------------
    #                                      CREATION OF ingr_storage.csv

    # Create the csv file and write the datas inside it. Note that Quantita is 0 everywhere in this file
    with open("ingr_storage.csv", "w", newline="", encoding="utf-8") as file:
        # Create first line of the csv file to give an idea of it content informations
        writer = csv.DictWriter(
            file, fieldnames=["Nome", "Quantita", "Unità di misura"]
        )
        writer.writeheader()
        # For each one ingredient
        for ingrediente in ingredienti:
            # Write a line with these informations
            writer.writerow(
                {
                    "Nome": ingrediente,
                    "Quantita": ingredienti[ingrediente]["Quantita"],
                    "Unità di misura": ingredienti[ingrediente]["Unità di misura"],
                }
            )

    # --------------------------------------------------------------------------------------------------------------
    #                                      CREATION OF ingr_storage1.csv

    # Create the csv file and write the datas inside it. Note that Quantita is 0 everywhere also in this file, but we can
    # then modify it manually, inserting some values for Quantita, in this way we can iniitialize a custom magazzino
    # from something like a checkpoint (a starting point)
    with open("ingr_storage1.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["Nome", "Quantita", "Unità di misura"]
        )
        writer.writeheader()
        for ingrediente in ingredienti:
            writer.writerow(
                {
                    "Nome": ingrediente,
                    "Quantita": ingredienti[ingrediente]["Quantita"],
                    "Unità di misura": ingredienti[ingrediente]["Unità di misura"],
                }
            )

    # --------------------------------------------------------------------------------------------------------------
    #                                      CREATION OF elenco_uso_ingredienti.csv

    # Create the csv file that stores a valure of the usage of different ingredients in different recipes
    with open("elenco_uso_ingredienti.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["Nome", "Unità di misura", "Contatore usi"]
        )
        writer.writeheader()
        for ingrediente in ingredient_usage_record:
            writer.writerow(
                {
                    "Nome": ingrediente,
                    "Unità di misura": ingredient_usage_record[ingrediente][
                        "Unità di misura"
                    ],
                    "Contatore usi": ingredient_usage_record[ingrediente][
                        "Contatore uso"
                    ],
                }
            )
    # --------------------------------------------------------------------------------------------------------------
    #                                   CREATION OF elenco_ingredienti.txt
    # --------------------------------------------------------------------------------------------------------------

    ingr_list = []
    # Put the key attribute of the ingredients dictionary, i.e. the name of the ingredient, inside ingredients_list
    ingredienti_list = list(ingredienti.keys())
    # Sort the list according to the lexicographic order
    ingredienti_list.sort()
    for ingrediente in ingredienti_list:
        # Remove any double spaces
        ing = ingrediente.strip().replace("  ", " ")
        # Remove any bees or double bees
        if ing.startswith('" '):
            ing = ing[2:]
        elif ing.startswith('"'):
            ing = ing[1:]

        # Remove the last double quote if present
        if ing.endswith(' "'):
            ing = ing[:-2]
        elif ing.endswith('"'):
            ing = ing[:-1]
        # Add ingredient name to list
        if ing not in ingr_list:
            ingr_list.append(ing)

    # Create the txt file that stores a valure of the usage of different ingredients in different recipes
    with open("elenco_ingredienti.txt", "w", encoding="utf-8") as file_output:
        for ingre in ingr_list:
            file_output.write(ingre.lower() + "\n")


# Need to add this
if __name__ == "__main__":
    main()
