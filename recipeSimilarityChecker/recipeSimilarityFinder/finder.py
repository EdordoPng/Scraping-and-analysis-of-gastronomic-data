import os
import pandas as pd
import configparser
import json

# ENG :

# This program takes care of simplifying the search for a certain flow rate within the csv file
# with all similarity values ​​between the respective recipes.
# To work properly, the user only needs to set the search parameters he wants
# in the finder.conf file, where it can also point to the recipe name

# ITA :

# Questo programma si occupa di andare a semplificare la ricera di una determinata portata all'interno del file csv
# con tutti i valori di similarità tra le rispettive ricette.
# Per funzionare correttamente, l'utente ha il solo bisogno di settare i parametri della ricera da lui desiderati
# all'interno del file finder.conf, in cui può indicare anche il nome della ricetta


def obtain_folder_informations():
    """Obtain useful informations from dataAnalysis.conf."""
    config = configparser.ConfigParser()
    # If the configuration file is not found, a new file is created
    if not os.path.isfile("finder.conf"):
        config["FOLDER TO ANALYZE"] = {
            "folder": "similarity_csv",
        }
        config["CSV TO ANALYZE"] = {
            "file": "antipasti.csv",
        }
        config["RECIPE TO ANALYZE"] = {
            "recipe": "",
        }
        with open("finder.conf", "w") as configfile:
            config.write(configfile)
        return "similarity_csv", "antipasti.csv", ""
    # If the configuration file exists, the name of the recipe to be analyzed is read from there
    else:
        config.read("finder.conf")
        folder = config["FOLDER TO ANALYZE"]["folder"]
        file = config["CSV TO ANALYZE"]["file"]
        recipe = config["RECIPE TO ANALYZE"]["recipe"]
        cookbook_folder = config["COOKBOOK FOLDER TO ANALYZE"]["folder"]
        cookbook_file = config["JSON COOKBOOK TO ANALYZE"]["file"]
        return folder, file, recipe, cookbook_folder, cookbook_file


def obtain_db(folder_name: str, json_name: str):
    """Get the database with all recipe informations and return this object"""
    os.chdir("..")
    os.chdir("..")

    # Move to work into cartella_portate and there open the requeste file
    os.chdir(folder_name)
    # Open the input file
    with open(json_name, "r", encoding="utf-8") as json_file:
        db_ricette = json.load(json_file)
    return db_ricette


def process_data(
    first_recipe_name: str,
    second_recipe_name: str,
    db_ricette,
):
    """Computes common ingredients between two recipes"""
    first_recipe_ingredients = []
    second_recipe_ingredients = []

    for ricetta in db_ricette:
        if ricetta["Titolo"].lower() == first_recipe_name:
            first_recipe_ingredients = [
                ingrediente["Nome"] for ingrediente in ricetta["Ingredienti"]
            ]

        if ricetta["Titolo"].lower() == second_recipe_name:
            second_recipe_ingredients = [
                ingrediente["Nome"] for ingrediente in ricetta["Ingredienti"]
            ]

    comuni = set(first_recipe_ingredients) & set(second_recipe_ingredients)
    return comuni


# Note that the file_name used here is that of the csv file in the .conf
def find_similar(recipe_name, file_name, cookbook_folder, cookbook_file):
    # Read CSV file and use recipe column as dataframe index
    df = pd.read_csv(file_name, index_col=0)

    db = obtain_db(cookbook_folder, cookbook_file)

    # Search recipes into the dataframe
    try:
        recipe_row = df.loc[recipe_name]
    except KeyError:
        print(
            "La ricetta '{}' non è presente nella tabella, controlla la correttezza del nome".format(
                recipe_name
            )
        )
        SystemExit

    # Discard values equals to 1
    recipe_row = recipe_row[recipe_row != 1]

    for idx, (recipe, similarity) in enumerate(
        recipe_row.sort_values(ascending=False)[:20].items(), start=1
    ):
        common_ingredients = process_data(
            recipe_name,
            recipe,
            db,
        )
        # Print on terminal obtained datas
        print(
            f"{idx}. {recipe} - Similarità: {similarity} - Ingredienti in comune: {', '.join(common_ingredients)}"
        )


def main():

    (
        folder_name,
        file_name,
        recipe_name,
        cookbook_folder,
        cookbook_file,
    ) = obtain_folder_informations()

    # Ci spostiamo nella cartella madre del file per cercare la cartella folder_name che contiene tutti i file CSV
    os.chdir("..")
    os.chdir(folder_name)
    # Start the computation
    find_similar(recipe_name, file_name, cookbook_folder, cookbook_file)


if __name__ == "__main__":
    main()
