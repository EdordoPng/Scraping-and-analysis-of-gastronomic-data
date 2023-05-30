import csv
from fuzzywuzzy import fuzz
import datetime
import os

# Use this program to obtain a list of parent ingredients, one for Planeat and one for Dissapore

# ENG:

# We're using 2 different files to fetch data from, these are :
#    - genitore_1_loro.csv      ------        Ingredienti che non abbiano un ingrediente genitore
#    - genitore_1_mio.csv       ------        Ingrediente contenuto nel nome di una ricetta

# When the program is configured, we get 1 csv output with information about the pairs in the cases:

#       - perfect matching of the two names (of ingredients in the two sets of main ingredients, mine and theirs)
#       - fuzzy matching of the two names (of ingredients in the two sets of main ingredients, mine and theirs

# Analyzed cases :
#       - PERFECT NAME MATCHING using genitore_1_loro and genitore_1_mio
#       - FUZZY NAME MATCHING using genitore_1_loro and genitore_1_mio

# ITA :

#       - matching perfetto dei due nomi (di ingredienti nei due set di ingredienti principali, miei e loro)
#       - fuzzy matching dei due nomi (di ingredienti nei due set di ingredienti principali, miei e loro

#       - PERFECT NAME MATCHING usando genitore_1_loro e genitore_1_mio
#       - FUZZY NAME MATCHING usando genitore_1_loro e genitore_1_mio

# This function takes two lists of ingredients as input, if an ingredient from one list is also used in the other
# according to a perfect mathing, if all the letters of the ingredient name are equal, if true then add the ingredient to the
# list which I'm then going to return.
def name_matching(ing_list_1, ing_list_2):
    """Find perfect name matching between ingredients from two lists."""
    counter = 0
    list = []
    for ingr1 in ing_list_1:
        if ingr1 in ing_list_2:
            if ingr1 not in list:
                counter = counter + 1
                list.append(ingr1)
    return list, counter


def check_fuzzy_match(stringa1, stringa2):
    """Function to compute fuzzy matching between two strings."""
    # Use the "ratio" method of the fuzzywuzzy library to calculate the similarity score
    # between the two strings, ranging from 0 (no similarity) to 100 (perfect similarity)
    return fuzz.ratio(stringa1.lower(), stringa2.lower())


def list_fuzzy_similarity(ingr_list_1, ingr_list_2, minimum_score: int):
    """Creates a list of all two ingredients name matching, based on a minimum input fuzzy score."""
    # Get the current date and time
    now = datetime.datetime.now()

    # Eventually use a counter to to track elements number
    counter = 0
    i = 0
    # Create a list to store the matched pairs of ingredients and fuzzy indexes
    matched_pairs = []

    # Iterate along srings into the array ingr_list_1. For each one of it elements, start a for loop to check if
    # the ingredient name has a fuzzy matching with some of the string inside the ingr_list_2
    for stringa1 in ingr_list_1:
        for stringa2 in ingr_list_2:
            # Check the fuzzy score of similarity
            score = check_fuzzy_match(stringa1, stringa2)

            if score >= minimum_score and score <= 100:
                # Append the matched pair of ingredients and fuzzy index to the list
                matched_pairs.append([stringa1, stringa2, score])
                # Increase the counter which tells me in total how many pairs will have been valid
                counter += 1
            # Increase the counter i which tells me in total how many pairs, valid and not, I have analysed
            if i % 100000 == 0:
                # Print time in "hh:mm:ss" format
                print(
                    "Orario corrente:",
                    now.strftime("%H:%M:%S"),
                    " siamo a tot elementi analizzati : ",
                    i,
                )
            i += 1
    return matched_pairs, counter


# Note that matched_pairs is the array returned by list_fuzzy_similarity
def csv_saving(fileName: str, matched_pairs, output_folder_name):
    """Create a csv file with two ingredients matching and score on each row"""
    # Check if the folder exists, if not create the folder cartella_portate
    if not os.path.exists(output_folder_name):
        os.makedirs(output_folder_name)
    # Move to work into it
    os.chdir(output_folder_name)
    # Write the matched pairs to a CSV file
    with open(fileName, mode="w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Ingrediente Lista 1", "Ingrediente Lista 2", "Indice di Fuzzy"]
        )
        for pair in matched_pairs:
            writer.writerow(pair)
    # Once finisched, come back
    os.chdir("..")


def main():
    # Name of the folder that we would use to gather input files
    FOLDER_NAME = "cartella_genitori"
    OUTPUT_FOLDER_NAME = "cartella_matching"
    # File name variables
    FILE_1 = "genitore_1_loro.csv"
    FILE_2 = "genitore_1_mio.csv"

    ingredienti_1_loro = []
    ingredienti_1_mio = []

    # Save into a variable the current working directory
    tsf = os.getcwd()
    # Move to work inside cartella_portate to gather the file Cookbook_SingleServing.json to obtain recipes informations
    os.chdir(FOLDER_NAME)

    # ---------------------------------------------- CSV opening ---------------------------------------------------
    with open(FILE_1, "r", encoding="utf-8") as file1, open(
        FILE_2, "r", encoding="utf-8"
    ) as file2:
        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)

        for row in reader1:
            ingredienti_1_loro.append(row[0])
        for row in reader2:
            ingredienti_1_mio.append(row[0])

    # Back to work into this script folder
    os.chdir("..")
    os.chdir(tsf)
    # -------------------------------------- Print len and how dataset where obtained---------------------------------------

    print("")
    print(
        f" Numero Ingredienti in ingredienti_1_loro : {len(ingredienti_1_loro)}      ------      Ingredienti che non abbiano un ingrediente genitore"
    )
    print(
        f" Numero Ingredienti in ingredienti_1_mio : {len(ingredienti_1_mio)}      ------      Ingrediente contenuto nel nome di una ricetta "
    )

    # ------------------------------------------- START PERFECT NAME MATCHING COMPUTATION ----------------------------------------
    print("")
    print("START PERFECT NAME MATCHING COMPUTATION")
    print("")
    # ------------------------------- CHECK NAME MATCHING : ingredienti_1_loro e ingredienti_1_mio
    lista_name_matching_1, counter = name_matching(
        ingredienti_1_loro, ingredienti_1_mio
    )
    print(
        f"Tra genitore_1_loro.csv e genitore_1_mio.csv gli ingredienti corrispondenti sono : {counter} "
    )
    # ------------------------------------------------ START FUZZY COMPUTATION ------------------------------------------------------
    print("")
    print("START FUZZY COMPUTATION")
    print("")

    # -------------------------------- CHECK FUZZY similarity : ingredienti_1_loro e ingredienti_1_mio ----------------------------------
    file3, ing_counter_3 = list_fuzzy_similarity(
        ingredienti_1_loro, ingredienti_1_mio, 80
    )
    csv_saving("parent_ingr_fuzzy_matching.csv", file3, OUTPUT_FOLDER_NAME)
    print(
        f"In parent_ingr_fuzzy_mathing ci sono : {ing_counter_3} ingr, usando una soglia fuzzy score >= 80  "
    )


# Need to add this
if __name__ == "__main__":
    main()
