import os
import json
import configparser

# ENG :

# This program gets the two recipes to compare from the commonIngredientsFinder.conf file, which can be
# changed to indicate the names of the two recipes to compare. Thus I obtain the ingredients in common with each other
# Using the name, the recipes are searched for in the Cookbook_SingleServing.json file, from which further data can be extrapolated
# This program is self-contained and can be called individually by configuring its .conf file

# ITA :

# Questo programma acquisisce le due ricette da confrontare dal file commonIngredientsFinder.conf , il quale può essere
# modificato per indicare i nomi delle due ricette da confrontare. Ottengo così gli ingredienti in comune tra loro
# Tramite il nome vengono ricercate le ricette nel file Cookbook_SingleServing.json, da cui si estrapolano ulteriori dati
# Questo programma è a se stante e puo esser chiamato singolarmente andando a configurare il suo file .conf


def obtain_folder_informations():
    """Ottiene informazioni utili dal file dataAnalysis.conf."""
    config = configparser.ConfigParser()
    # If the configuration file is not found, a new file is created
    if not os.path.isfile("commonIngredientsChecker.conf"):
        config["FOLDER TO ANALYZE"] = {
            "folder": "cartella_portate",
        }
        config["CSV TO ANALYZE"] = {
            "file": "Cookbook_SingleServing.json",
        }
        config["RECIPE TO ANALYZE"] = {
            "recipe1": "",
            "recipe2": "",
        }
        with open("commonIngredientsChecker.conf", "w") as configfile:
            config.write(configfile)
        return "cartella_portate", "Cookbook_SingleServing.json", "", ""
    # If the configuration file exists, the name of the recipe to be analyzed is read from there
    else:
        config.read("commonIngredientsChecker.conf")
        folder = config["FOLDER TO ANALYZE"]["folder"]
        file = config["JSON TO ANALYZE"]["file"]
        recipe1 = config["RECIPE TO ANALYZE"]["recipe1"]
        recipe2 = config["RECIPE TO ANALYZE"]["recipe2"]

        return folder, file, recipe1, recipe2


def process_data(
    folder_name: str, json_name: str, first_recipe_name: str, second_recipe_name: str
):
    """Return common and uncommon ingredients betwenn two recipes, separately"""
    os.chdir("..")
    # Move to work into cartella_portate and there open the requeste file
    os.chdir(folder_name)
    with open(json_name, "r", encoding="utf-8") as json_file:
        db_ricette = json.load(json_file)
    # Declare variables
    first_recipe_ingredients = []
    second_recipe_ingredients = []

    for ricetta in db_ricette:
        if ricetta["Titolo"] == first_recipe_name:
            first_recipe_ingredients = [
                ingrediente["Nome"] for ingrediente in ricetta["Ingredienti"]
            ]

        if ricetta["Titolo"] == second_recipe_name:
            second_recipe_ingredients = [
                ingrediente["Nome"] for ingrediente in ricetta["Ingredienti"]
            ]
    # Common elements to both datasets
    comuni = sorted(set(first_recipe_ingredients) & set(second_recipe_ingredients))
    # Not Common elements to both datasets
    non_comuni = sorted(
        set(
            [
                f"{x} - {first_recipe_name}"
                for x in first_recipe_ingredients
                if x not in comuni
            ]
        )
        ^ set(
            [
                f"{x} - {second_recipe_name}"
                for x in second_recipe_ingredients
                if x not in comuni
            ]
        )
    )

    return comuni, non_comuni


def easy_process_data(first_recipe_name: str, second_recipe_name: str):
    """Simplified variant of process_data(...) to be used quickly"""
    process_data(
        "cartella_portate",
        "Cookbook_SingleServing.json",
        first_recipe_name,
        second_recipe_name,
    )


# Definition of the main function that will be called once user run the program
def main():
    (
        folder_name,
        json_name,
        first_recipe_name,
        second_recipe_name,
    ) = obtain_folder_informations()

    comuni, non_comuni = process_data(
        folder_name, json_name, first_recipe_name, second_recipe_name
    )

    print("---------------- Gli ingredienti COMUNI sono : ----------------")
    for ingrediente in comuni:
        print(ingrediente)
    print("---------------- Gli ingredienti NON COMUNI sono : ----------------")
    for ingrediente in non_comuni:
        print(ingrediente)


# Need to add this
if __name__ == "__main__":
    main()
