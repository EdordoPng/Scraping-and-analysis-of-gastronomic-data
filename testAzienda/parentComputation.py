import csv
import os
import json

# ENG :

# This program has the purpose of creating :
#       - two csv files, they will contain the primary ingredient list, one for planeat and one for dissapore
#       - two txt files, they will contain the total ingredient list, one for planeat and one for dissapore

# ITA :

# Questo programma mira a creare:
#       - due file csv, conterranno l'elenco degli ingredienti primari, uno per planetat e uno per dissapore
#       - due file txt, conterranno la lista totale degli ingredienti, uno per planetat e uno per dissapore


# Name of the folder that we would use as ontainer of output files
FOLDER_NAME = "cartella_genitori"
PRIMARY_PLANEAT_INGREDIENTS_NAME = "primary_Planeat_ingredients.CSV"
PRIMARY_DISSAPORE_INGREDIENTS_NAME = "primary_Dissapore_ingredients.csv"

# Checks if the folder that contains needed files exists
def check_folder():
    """Checks folder existence"""
    # Check if the folder exists, if not create the folder cartella_portate
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)


# Analyze my file containing all the recipes and choose some primary ingredients based on whether the name
# of the ingredient or part of it, are a substring of the recipe title
def genitore_1_mio(folderName: str, fileName: str):
    """Open fileName and obtain a csv with datas from my recipe jsons"""
    ingredienti = set()
    # Name of output csv file
    file_name = PRIMARY_DISSAPORE_INGREDIENTS_NAME
    # This script folder, save the variable to use later
    tsf = os.getcwd()
    # Move to work inside cartella_portate to gather the file Cookbook_SingleServing.json to obtain recipes informations
    os.chdir("..")
    os.chdir(folderName)

    # Read json file
    with open(fileName, "r", encoding="utf-8") as json_file:
        db_ricette = json.load(json_file)

    # Back to work into this script folder
    os.chdir("..")
    os.chdir(tsf)

    # Iterate along reipes
    for recipe in db_ricette:
        # Convert the recipe title to lowercase so that it compares with the recipe names
        # ingredients as these are also in lower case
        Titolo_ricetta = recipe["Titolo"].lower()
        # For each recipe ingredient
        for ingredient in recipe["Ingredienti"]:
            # Get the name of the ingredient in a variable, removing any double spaces so as to
            # have well formatted strings without this problem
            ingredient_name = ingredient["Nome"].strip().replace("  ", " ")
            # Make the ingredient name lowercase so it's easy to match the title of the recipe as this is also in lowercase
            ingredient_name = ingredient_name.lower()
            # If this condition is true, then the ingredient is conceivable as primary.
            # I could go to see how many duplicates there are in this list to see how many times a primary ingredient is used
            # and have an idea of ​​the most used ones.
            # Check if the name is included in the recipe title or if part of the ingredient name is in the recipe title

            if (
                ingredient_name in Titolo_ricetta
                or ingredient_name.split()[0][:-1] in Titolo_ricetta
            ):
                # This way I avoid having duplicates. That's because I want a list of all the primary ingredients I can find
                # like this. The code can be used to find the primary ingredients for any recipe
                if ingredient_name not in ingredienti:
                    ingredienti.add(ingredient_name)
    # Sort ingredients according to the lexicographic order
    ingredienti_ordinati = sorted(ingredienti)

    # Check if the folder exists, if not create the folder cartella_portate
    check_folder()
    # Create the path
    file_path = os.path.join(FOLDER_NAME, file_name)
    # Create the csv file that contains my primary ingredients
    with open(file_path, mode="w", newline="", encoding="utf-8") as file_output:
        writer = csv.writer(file_output)
        for ingrediente in ingredienti_ordinati:
            writer.writerow([ingrediente])
    print(f"File csv : {file_path} has been succesfully created.")

    # Restore the set so as not to dirty any subsequent jobs
    ingredienti = set()


# Analyze their file containing all their ingredients, choose some primary ingredients based on the fact that
# have equal to "", i.e. empty, the field in which so finds the id of the parent ingredient from which they derive.
# Ingredients that do not have a parent ingredient
def genitore_1_loro(fileName: str):
    """Open fileName and obtain a csv with datas from their ingredients file"""
    ingredienti = set()
    file_name = PRIMARY_PLANEAT_INGREDIENTS_NAME
    # Open the csv file
    with open(fileName, encoding="utf-8") as file_csv:
        reader = csv.DictReader(file_csv)
        for row in reader:
            # Check for the absence of a parent ingredient with this statement
            if row["prime_item_id"] == "":
                # Make sure there are no double spaces
                ingredient_name = row["ingredient_name"].strip().replace("  ", " ")
                # Avoid duplicates
                if ingredient_name not in ingredienti:
                    ingredienti.add(ingredient_name)
    # Sort ingredients according to the lexicographic order
    ingredienti_ordinati = sorted(ingredienti)

    # Check if the folder exists, if not create the folder cartella_portate
    check_folder()
    # Create the path
    file_path = os.path.join(FOLDER_NAME, file_name)

    # Create the csv file that contains their primary ingredients
    with open(file_path, mode="w", newline="", encoding="utf-8") as file_output:
        writer = csv.writer(file_output)
        for ingrediente in ingredienti_ordinati:
            writer.writerow([ingrediente])
    print(f"File csv : {file_path} has been succesfully created.")

    # Restore the set so as not to dirty any subsequent jobs
    ingredienti = set()


# Parse their file containing all their ingredients, get all ingredient names without duplicates
# and put them in an output txt file
# Ingredient names and that's it
def all_planeat_ing(fileName: str):
    """Open fileName and obtain a txt with their all ingredients list"""
    ingredienti = set()
    file_name = "all_planeat_ing.txt"
    with open(fileName, encoding="utf-8") as file_csv:
        reader = csv.DictReader(file_csv)
        for row in reader:
            # Make sure there are no double spaces
            ingredient_name = row["ingredient_name"].strip().replace("  ", " ")
            # Make sure there are no double quotes in strings
            ingredient_name = ingredient_name.strip().replace('"', "")
            # Avoid duplicates
            if ingredient_name not in ingredienti:
                ingredienti.add(ingredient_name)
    # Sort ingredients according to the lexicographic order
    ingredienti_ordinati = sorted(ingredienti)
    # Check if the folder exists, if not create the folder cartella_portate
    check_folder()
    # Create the path
    file_path = os.path.join(FOLDER_NAME, file_name)
    # Create the txt file that contains their ingredients
    with open(file_path, mode="w", encoding="utf-8") as file_output:
        for ingrediente in ingredienti_ordinati:
            file_output.write(ingrediente + "\n")
    print(f"File txt : {file_path} has been succesfully created.")

    # Restore the set so as not to dirty any subsequent jobs
    ingredienti = set()


# Analyze my file containing all the recipes and find a list of all used ingredients
def all_dissapore_ing(folderName: str, fileName: str):
    """Open fileName and obtain a txt with my all ingredients list"""

    # Name of output txt file
    FILE_NAME = "all_dissapore_ing.txt"

    ingredienti = set()
    # This script folder, save the variable to use later
    tsf = os.getcwd()
    # Move to work inside cartella_portate to gather the file Cookbook_SingleServing.json to obtain recipes informations
    os.chdir("..")
    os.chdir(folderName)

    # Read json file
    with open(fileName, "r", encoding="utf-8") as json_file:
        db_ricette = json.load(json_file)
    # Back to work into this script folder
    os.chdir("..")
    os.chdir(tsf)

    # Iterate along reipes
    for recipe in db_ricette:
        for ingredient in recipe["Ingredienti"]:
            # Make sure there are no double spaces
            ingredient_name = ingredient["Nome"].strip().replace("  ", " ")
            # Make the ingredient name lowercase so it's easy to match the title
            # of the recipe as this is also in lowercase
            ingredient_name = ingredient_name.lower()
            # Avoid duplicates
            if ingredient_name not in ingredienti:
                ingredienti.add(ingredient_name)
    # Sort ingredients according to the lexicographic order
    ingredienti_ordinati = sorted(ingredienti)

    # Check if the folder exists, if not create the folder cartella_portate
    check_folder()
    # Create the path
    file_path = os.path.join(FOLDER_NAME, FILE_NAME)
    # Create the txt file that contains all mine ingredients
    with open(file_path, mode="w", encoding="utf-8") as file_output:
        for ingrediente in ingredienti_ordinati:
            file_output.write(ingrediente + "\n")
    print(f"File txt : {file_path} has been succesfully created.")

    # Restore the set so as not to dirty any subsequent jobs
    ingredienti = set()


def main():
    pass

    # DECOMMENTARE LA FUNZIONE CHE SI DESIDERA ESEGUIRE

    print("COMPUTAZIONE INIZIATA genitore 1 loro")
    genitore_1_loro("ingredienti-planeat.csv")

    print("COMPUTAZIONE INIZIATA genitore 1 mio")
    genitore_1_mio("cartella_portate", "Cookbook_SingleServing.json")

    print("COMPUTAZIONE INIZIATA all_planeat_ing")
    all_planeat_ing("ingredienti-planeat.csv")

    print("COMPUTAZIONE INIZIATA all_dissapore_ing")
    all_dissapore_ing("cartella_portate", "Cookbook_SingleServing.json")


# Need to add this
if __name__ == "__main__":
    main()
