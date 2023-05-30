import os
import json
import csv
import pandas as pd

# ENG :

# This program finds the recipes that can be made, checking the ingredients and evaluating possible substitutes
# present in the fuzzy matching file. The one used in this case is testCompany/folder_matchingcomplete_fuzzy2.csv
# That file is produced by the program that uses the best performing model among the 6 created in testCompany (reference
# a completeFuzzy.py , completeFuzzy2.py , ... , completeFuzzy6.py ), among which the second was the most performing

# ITA :

# Questo programma trova le ricette che possono esser realizzate, controllando gli ingredienti e valutando eventuali sostituti
# presenti nel file di fuzzy matching. Quello utilizzato in questo caso è testAzienda/cartella_matching/complete_fuzzy2.csv
# Quel file viene prodotto dal programma che sfrutta il modello più performante tra i 7 creati in testAzienda (riferimento
# a completeFuzzy.py , completeFuzzy2.py , ... , completeFuzzy6.py ), tra i quali il secondo è risultato il più performante.

# Need this function cause elenco_ingredienti.txt contains a list of all ingredient used into the cookbook file
def open_txt(input_file_name_: str):
    """Open a txt file to gather all ingredients list"""
    # Create the dataset
    ingredienti = set()
    # Open txt
    with open(input_file_name_, encoding="utf-8") as file_txt:
        for row in file_txt:
            # Avoid duplicates
            ingredient_name = row.strip()
            if row not in ingredienti:
                ingredienti.add(ingredient_name)
    return sorted(ingredienti)


# Function to check missing ingredients. It returns ricDisp, the craftable recipes (ricette realizzabili)
def checker_ingr_ricetta(ric, planeat_ingredient_list, complete_fuzzy):
    """Check the presence of recipe's ingredient inside the storage."""
    recipe_title = ric["Titolo"]
    # Basic ingredients that people usually have at home
    ingredienti_che_si_hanno_a_casa = [
        "sale",
        "pepe",
        "pepe nero",
        "sale fino",
        "sale grosso",
        "olio",
        "olio evo",
        "olio di semi",
        "olio di semi di sesamo",
        "olio di semi per friggere",
        "aceto di vino bianco",
        "aceto",
        "zucchero",
        "zucchero di canna",
        "rosmarino",
    ]

    # Initialize a list to contein all missing ingredients
    ingredienti_mancanti = []
    ingredienti_sostituti = []
    # Fuzzy similarity index
    indice_fuzzy = 0
    # Iterate along every ingredient of the recipe
    for ingrediente_ricetta in ric["Ingredienti"]:
        ingredient_name = ingrediente_ricetta["Nome"].lower()

        # Check if the ingredient's name is inside the list of available ingredients
        if (
            ingredient_name in planeat_ingredient_list
            or ingredient_name in ingredienti_che_si_hanno_a_casa
        ):
            continue
        else:

            # ENG
            # I want and give to find all occurrences of ingredient_name in complete_fuzzy.iloc[:, 1].values
            # and don't stop me only at the first one. Collected the list of tuples that repeat this requirement,
            # I want to choose the tuple that maximizes the fuzzy score, i.e. the number in the third column.

            # ITA
            # Voglio anddare a trovare tutte le evenienze di ingredient_name in complete_fuzzy.iloc[:, 1].values
            # e non andarmi a fermare solo alla prima. Collezionato l'elenco di tuple che ripechiano questo requisito,
            # voglio andare a scegliere la tupla che massimizza il fuzzy score, ossia il numero sulla terza colonna.

            # Find all occurrences of ingredient_name in complete_fuzzy.iloc[:, 1].values
            matching_rows = complete_fuzzy[
                complete_fuzzy.iloc[:, 1].str.contains(ingredient_name, case=False)
            ]

            # Select the row with the maximum Fuzzy score
            if not matching_rows.empty:
                best_match = matching_rows.loc[
                    matching_rows.iloc[:, 2].astype(float).idxmax()
                ]

                # print(best_match)
                ingredienti_sostituti.append(
                    (
                        f"Ingrediente Dissapore da sostituire : {ingredient_name}",
                        f"Ingrediente Planeat Sostituto : {best_match[0]}",
                        f"Fuzzy Score : {best_match[2]}",
                    )
                )

                indice_fuzzy = indice_fuzzy + 1
                continue
            else:
                # Else the ingredient will be appended to the missing ingredients list
                ingredienti_mancanti.append(ingredient_name)

    print(f"Ingredienti mancanti per : {recipe_title}")
    print(ingredienti_mancanti)
    # I print planetat substitute ingredients only if there are any
    if indice_fuzzy != 0:
        print(f"Ingredienti Sostituti per : {recipe_title}, sono : {indice_fuzzy}")
        print(ingredienti_sostituti)

    print("")

    # Check if the recipe has some missing ingredient. If not, the recipe will be added to the available recipes list
    if len(ingredienti_mancanti) == 0:
        # Maybe sometimes a recipe could be inside different Portata. So if it's already there, don't add it
        return recipe_title
    else:
        return ""


def apri_complete_fuzzy_csv():
    """Open in read mode the csv with all matching found using the designed methodology"""
    complete_fuzzy = []
    current_directory = os.getcwd()
    os.chdir("..")
    os.chdir("testAzienda")
    os.chdir("cartella_matching")
    with open("complete_fuzzy2.csv", "r", encoding="utf-8-sig") as f:
        data = list(csv.DictReader(f))
        # Adding data to the recipe list
        complete_fuzzy.extend(data)

    # make it a pandas deataframe
    complete_fuzzy = pd.DataFrame(complete_fuzzy)

    os.chdir("..")
    os.chdir("..")
    os.chdir(current_directory)

    return complete_fuzzy


# Function that returns a list of the realizable recipes with the ingredients inside the storage
def ricette_realizzabili(db_ricette, planeat_ingredient_list):
    """Find the craftable recipe list based on the ingredient list."""
    # Declare a list of recipes that will be updated when a recipe is verified
    ricetteDisponibili = []
    # Get the pairs in a pandas dataframe
    complete_fuzzy = apri_complete_fuzzy_csv()

    # Iterate along the recipes
    for ricetta in db_ricette:

        recipe_name = checker_ingr_ricetta(
            ricetta, planeat_ingredient_list, complete_fuzzy
        )
        # If the recipe name is not a blank string, taht for the logic used in checker_ingr_ricetta means we doesn't
        # have alla the ingredients to create that recipe, than not add it to the creaftable recipes list
        if recipe_name != "" and recipe_name not in ricetteDisponibili:
            ricetteDisponibili.append(recipe_name)

    # Return the dictionary variable
    return ricetteDisponibili


def main():
    # txt file with a list of all ingredients used into Planeat recipes
    NOME_FILE_TXT = "all_planeat_ing.txt"
    # Folder that contains the csv file with the couples of ingredient from different dataset, and the score of similatiry
    NOME_CARTELLA_1 = "testAzienda"
    NOME_CARTELLA_2 = "cartella_genitori"

    script_folder = os.getcwd()
    os.chdir("..")
    os.chdir(NOME_CARTELLA_1)
    os.chdir(NOME_CARTELLA_2)

    # Get a list of available ingredients
    planeat_ingredients = open_txt(NOME_FILE_TXT)
    os.chdir("..")
    os.chdir("..")
    os.chdir("cartella_portate")

    # I'm going to open my json file on all recipes
    with open("Cookbook_SingleServing.json", "r", encoding="utf-8") as json_file:
        db_ricette = json.load(json_file)
    os.chdir("..")
    os.chdir(script_folder)

    # Once ingredients and db_recipes have been obtained, you need to scroll through the various recipes and see which
    # ones are creaftable with ingredients in planetat_ingredients
    available_reipes = ricette_realizzabili(db_ricette, planeat_ingredients)

    # We print the titles of the recipes and with them if they are feasible or not,
    # the missing ingredients and any substitute ingredients

    print("Ricette realizzabili con ingredienti Planeat : ")
    for ric in available_reipes:
        print(ric)
    print(
        "Numero totale ricette realizzabili con ingredienti Planeat : ",
        len(available_reipes),
    )
    print("Numero totale di ricette Dissapore : ", len(db_ricette))


# Need to add this
if __name__ == "__main__":
    main()
