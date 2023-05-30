import json
import pandas as pd
import numpy as np
import os
import datetime
import sys
import configparser
from scipy.sparse import lil_matrix
from sklearn.metrics.pairwise import cosine_similarity

# ENG :

# This program has the purpose of creating similarity dataframe for each Portata analyzed. Thge similarity score between two different
# recipes is obtained checking firstly the cosine similarity between ingredients dataset of each recipe with others.
# Then this value is updated using a logic that expects :
#   - To Find : Primary ingredients of a recipe
#       (ingredients with the name or part of their name are contained in the name of the recipe to which they belong)
#   - To Find : Primary ingredients in common and not common between trwo recipes
#   - Compute : How much totaal Primary ingredients are and obtain the new updated value

# ITA :

# Questo programma ha lo scopo di creare un dataframe di similarità per ogni Portata analizzata.
# Il punteggio di somiglianza tra due diverse ricette, viene ottenuto controllando in primo luogo la similarità coseno
# tra gli ingredienti di ciascuna ricetta con gli altri.
# Quindi questo valore viene aggiornato utilizzando una logica che prevede di andare a :
#   - trovare: gli ingredienti primari di una ricetta
#       (gli ingredienti con il nome o parte del loro nome sono contenuti nel nome della ricetta a cui appartengono)
#   - trovare: ingredienti primari in comune e non in comune tra due ricette
#   - calcolare: quanti sono gli ingredienti primari totali e ottienere il nuovo valore aggiornato


# CSV files folder name
NOME_CARTELLA_CSV = "similarity_csv"

# XLSX files folder name
NOME_CARTELLA_XLSX = "similarity_xlsx"


def obtain_informations():
    """Obtain useful datas form the dataAnalysis.conf file."""
    # Initialyze the parser
    config = configparser.ConfigParser()
    # If conf file not found, then close the program
    if not os.path.isfile("similarityChecker.conf"):
        sys.exit("Not found the similarityChecker.conf file")
    # If the conf is found, then take folder and portatas json file names that needs to be analyzed
    else:
        config.read("similarityChecker.conf")
        portata_folder = config["FOLDER TO ANALYZE"]["folder"]
        portate_to_analyze = []
        for key in config["JSON TO ANALYZE"]:
            portate_to_analyze.append(config["JSON TO ANALYZE"][key])
        cookbook_folder = config["COOKBOOK FOLDER TO ANALYZE"]["folder"]
        cookbook_file = config["JSON COOKBOOK TO ANALYZE"]["file"]

        return portata_folder, portate_to_analyze, cookbook_folder, cookbook_file


def apri_ricettario(folder_name: str, json_name: str):
    """Obtain a dict of usefoul recipe datas form the recipe json file"""
    # Move to work in folder_name folder and then open the requested json
    os.chdir("..")
    os.chdir(folder_name)
    with open(json_name, "r", encoding="utf-8") as json_file:
        db_ricette = json.load(json_file)

    # Create a dict to store recipes with recipe name as key
    ricette_dict = {}

    # Iterate along all recipes
    for ricetta in db_ricette:
        # Save the recipe name as low camel case string
        titolo = ricetta["Titolo"].lower()
        # Obtain the list of ingredients
        ingredienti_ricetta = ricetta["Ingredienti"]

        ricette_dict[titolo] = []
        # Add only the ingredient name and not other datas
        for i in ingredienti_ricetta:
            ricette_dict[titolo].append(i["Nome"].lower())
    # Back to work into mother folder
    os.chdir("..")
    # Return the recipes dict
    return ricette_dict


# Takes two recipes name and a dict, with recipe names as key, that contains all recipes and linked ingredients
def process_data(first_recipe_name: str, second_recipe_name: str, db_ricette):
    """Find common and non common ingredients between two recipes."""

    first_recipe_ingredients = []
    second_recipe_ingredients = []
    # Take the titles of the two riettes that I pass as input to the function and I get the lowercase version
    # Convert input recipe names into a lower camel case string
    first_recipe_name_minuscolo = first_recipe_name.lower()
    second_recipe_name_minuscolo = second_recipe_name.lower()
    # Fill the arrays
    for ingrediente in db_ricette[first_recipe_name_minuscolo]:
        first_recipe_ingredients.append(ingrediente.lower())
    for ingrediente in db_ricette[second_recipe_name_minuscolo]:
        second_recipe_ingredients.append(ingrediente.lower())

    # Find common elements between two datasets
    comuni = set(first_recipe_ingredients) & set(second_recipe_ingredients)
    # Find non common elements between two datasets. Note that ^ means "XOR"
    non_comuni = set(
        [(f"{x} Prima ricetta : {first_recipe_name}") for x in first_recipe_ingredients]
    ) ^ set(
        [
            (f"{x} Seconda ricetta : {second_recipe_name}")
            for x in second_recipe_ingredients
        ]
    )
    # Obtain primary ingredients of the two recipes
    first_recipe_primary_ingr = check_nome_ingr_in_title(
        first_recipe_name, first_recipe_ingredients
    )
    second_recipe_primary_ingr = check_nome_ingr_in_title(
        second_recipe_name, second_recipe_ingredients
    )

    (
        ingredienti_primari_in_comune,
        ingredienti_primari_non_in_comune,
    ) = check_primari_comuni(first_recipe_primary_ingr, second_recipe_primary_ingr)

    return (
        comuni,
        non_comuni,
        ingredienti_primari_in_comune,
        ingredienti_primari_non_in_comune,
    )


def ottieni_contributo(
    ingredienti_primari_in_comune,
    ingredienti_primari_non_in_comune,
    old_similarity_value,
):
    """Find thw right value that comes from presence or not of the principal ingredients. Uses an old value to update it."""

    # Find the complete number of primary ingredients between two recipes
    tot_ingr_prim = len(ingredienti_primari_in_comune) + len(
        ingredienti_primari_non_in_comune
    )
    # If no one primary ingredient has been found, then we return a 0 value. This mean that old_similarity_value will be
    # only sliced by two, cause the primary ingredient is 0
    if tot_ingr_prim == 0:
        return 0
    # Obtain the % of how mucch primary ingredients are in common (verus how much primary ingredients there are
    percentuale_ingr_prim_in_comune = len(ingredienti_primari_in_comune) / tot_ingr_prim
    # Truncate to two decimal places
    percentuale_arrotondata = round(percentuale_ingr_prim_in_comune, 2)

    # Add the contributions and update the value to insert in the cell
    valore = percentuale_arrotondata + old_similarity_value

    # Divide by 2 and the round the resulto top the second decimal number beyond the comma
    valore = round(valore / 2, 2)

    return valore


# Find common and non-common primary ingredients, starting from two ingredient lists
def check_primari_comuni(ingredienti_primari_ricetta1, ingredienti_primari_ricetta2):
    """Find primarty ingredients in common and non common between two recipes."""

    # Find primary ingredients in common
    ingredienti_primari_in_comune = set(ingredienti_primari_ricetta1) & set(
        ingredienti_primari_ricetta2
    )

    # Find primary ingredients not in common
    ingredienti_primari_non_in_comune = set(ingredienti_primari_ricetta1) ^ set(
        ingredienti_primari_ricetta2
    )
    return (
        ingredienti_primari_in_comune,
        ingredienti_primari_non_in_comune,
    )


# Use this function to check if the name of an ingredient or part of it is contained within the title
# of the recipe to which this ingredient belongs
def check_nome_ingr_in_title(recipe_name: str, ingredient_list: list):
    """Find if ingredient name is inside the recipe name."""
    # Create a list of primary ingredients
    primary_ingredient_list = []
    # Iterate along the input ingredient list
    for ing in ingredient_list:
        # If the ingredient name or part of it is found inside the recipe name (not nonsidering the last letter of the ingredient name)
        if ing in recipe_name or ing.split()[0][:-1] in recipe_name:
            # If not already added
            if ing not in primary_ingredient_list:
                primary_ingredient_list.append(ing)
    return primary_ingredient_list


def check_similarita_base(file: str, folder_name: str):
    """Compute and return the similarity matrix for a Portata. this is a first stage matrix that needs to be updated."""
    # Save this script folder name
    script_folder = os.getcwd()
    # With this instruction we move to work into the mother folder of this file, because I need to search the folder_name folder
    # that contains all the json files extracted, one for each Portata
    os.chdir("..")
    # Move to work into cartella_portate and there open the requeste file
    os.chdir(folder_name)

    with open(file, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    # Create a list of ingredients for each recipe
    ingredienti = []
    for ricetta in data:
        for ingrediente in ricetta["ingredients"]:
            # For every ingredient we collect the name and format it to be without double blank spaces inside the name
            ingredient_name = ingrediente["name"].strip().replace("  ", " ")
            # Same done to the recipe title
            recipe_name = ricetta["title"].strip().replace("  ", " ")
            # Add the ingredients, in low camel letter case, to the list
            ingredienti.append((recipe_name.lower(), ingredient_name.lower()))

    # Get unique recipe and ingredient names
    ricette = list(set([ricetta[0] for ricetta in ingredienti]))
    # Get recipes lexicographicly sorted
    ricette = sorted(ricette)

    # Create a list of unique ingredients extracted from the recipe dataset
    ingredienti_unique = list(set([ingrediente[1] for ingrediente in ingredienti]))

    # Create a dictionary to map recipe and ingredient names to indices
    ricette_dict = {ricetta: i for i, ricetta in enumerate(ricette)}
    ingredienti_dict = {
        ingrediente: i for i, ingrediente in enumerate(ingredienti_unique)
    }

    # Create a sparse matrix of recipe-ingredient counts
    matrice = lil_matrix((len(ricette), len(ingredienti_unique)), dtype=np.int8)
    for ricetta, ingrediente in ingredienti:
        matrice[ricette_dict[ricetta], ingredienti_dict[ingrediente]] += 1

    # Compute cosine similarity matrix
    similarita = cosine_similarity(matrice)

    # Normalize similarity matrix by column max
    max_col = np.amax(similarita, axis=0)
    similarita = np.divide(similarita, max_col)
    # Round the number
    similarita = similarita.round(2)

    # Get recipe names as list of strings
    nomi_ricette = [str(ricetta) for ricetta in ricette]

    # Create DataFrame from similarity matrix and recipe names
    df_similarita = pd.DataFrame(similarita, columns=nomi_ricette, index=nomi_ricette)

    # Go back into parent directory
    os.chdir("..")
    # Move to work into this script folder. Becouse decided to store the csv file created here into the same of this script folder
    os.chdir(script_folder)

    return df_similarita


def check(
    portata_file: str, folder_name: str, cookbook_folder: str, cookbook_file_name: str
):
    """Compute and return the final similarity matrix for a Portata"""
    # Save this script folder name
    script_folder = os.getcwd()
    # Variable to take track of time
    now = datetime.datetime.now()
    # Variable counter to take track of the number of element analyzed
    count = 0
    # Obtain the dataframe with the base similarity matrix
    df_similarita = check_similarita_base(portata_file, folder_name)

    # Open the recipe book so as to open the json file that contains all the recipes in this way
    # to get a dictionary with recipe name key
    db_recipe = apri_ricettario(cookbook_folder, cookbook_file_name)

    print(f" Started Analysis for : {portata_file}")

    # Use these ranges to analyze only the higher triagle matrix above the principal diagonal
    for i in range(len(df_similarita)):
        for j in range(i + 1, len(df_similarita)):
            # Exclude the main diagonal from the analysis
            if i != j:
                # Obtain considered coloumn name
                colonna = df_similarita.columns[j]
                # Obtain considered row name
                index = df_similarita.index[i]

                # Save in a variable the old value of the cell indicated by column and index in df_similarity
                old_similarity_value = df_similarita.iloc[i, j]

                # Get the list of common and uncommon ingredients for the two recipes, ditto for the primary ones
                # Note that comuni and non comuni list are not used yet, due to lack of usefulness
                (
                    comuni,
                    non_comuni,
                    ingredienti_primari_in_comune,
                    ingredienti_primari_non_in_comune,
                ) = process_data(colonna, index, db_recipe)

                value = ottieni_contributo(
                    ingredienti_primari_in_comune,
                    ingredienti_primari_non_in_comune,
                    old_similarity_value,
                )

                # Set the new value to the specific cell in the dataframe
                df_similarita.at[index, colonna] = value

                # Here we're going to include a counter that allows us to keep track of the current iteration
                if count % 50000 == 0:
                    print(
                        "Orario corrente:",
                        now.strftime("%H:%M:%S"),
                        " siamo a tot elementi analizzati : ",
                        count,
                    )
                count += 1

    # Calculate the changes on the upper half of the dataframe
    for i in range(len(df_similarita)):
        for j in range(i + 1, len(df_similarita)):
            # Copy value from top half to bottom half
            df_similarita.iloc[j, i] = df_similarita.iloc[i, j]

    print(f" Analisi completata per : {portata_file}")
    print(f" Similarità analizzate  : {count}")

    # Go back into parent directory
    os.chdir("..")
    # Move to work into this script folder. Becouse decided to store the csv file created here into the same of this script folder
    os.chdir(script_folder)

    return df_similarita


def save_files(dataFrame, portata_name):
    """Save the dataFrame inside a CSV and a XLSX file, in respective folders."""

    #                                CSV File
    # Check existance of the similarity folder that will contain the csv files
    if not os.path.exists(NOME_CARTELLA_CSV):
        os.makedirs(NOME_CARTELLA_CSV)
    # Move into the CSV files folder
    os.chdir(NOME_CARTELLA_CSV)
    # Save DataFrame into a CSV file
    dataFrame.to_csv(portata_name + ".csv")
    # Back to work in this script folder
    os.chdir("..")

    #                               XLSX File
    # Check existance of the similarity folder that will contain the xlsx files
    if not os.path.exists(NOME_CARTELLA_XLSX):
        os.makedirs(NOME_CARTELLA_XLSX)
    # Move into the CSV files folder
    os.chdir(NOME_CARTELLA_XLSX)
    # Save DataFrame into a EXCEL file
    dataFrame.to_excel(portata_name + ".xlsx")
    # Back to work in this script folder
    os.chdir("..")


def main():
    # Setup variables
    folder_name, array_portate, cookbook_folder, cookbook_file = obtain_informations()

    for portata in array_portate:
        # Obtain the wanted similarity table
        df = check(portata, folder_name, cookbook_folder, cookbook_file)

        # Obtain only the name without the extension
        only_portata_name = portata.split(".")[0]
        # Save files as csv and xlsx
        save_files(df, only_portata_name)


# Need to add this
if __name__ == "__main__":
    main()
