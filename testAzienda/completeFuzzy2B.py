import csv
from fuzzywuzzy import fuzz
import datetime
import os

# Questo programma mi fornisce già un fuzzy più attento e complesso, uguale al 2 solo che qai invece di resituire 0 se la
# prima parola non matacha, qui resitituisco il valore della fuzzy similarity normale

# Use this program to go and compare all my ingredients with all of the company's to try to find matches. Save the output in a csv file

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


# A FRONTE DEI RISULTATI è MEGLIO QUELLO CHE CONTROLLA SENZA L'ULTIMA LETTERA DELLA PRIMA PAROLA

# def check_fuzzy_match(stringa1, stringa2):
#    """Function to compute fuzzy matching between two strings."""
#    # Split the strings into tokens and compare the sorted tokens
#    tokens1 = stringa1.lower().split()
#    tokens2 = stringa2.lower().split()
#    sorted_tokens1 = sorted(tokens1)
#    sorted_tokens2 = sorted(tokens2)
#    if sorted_tokens1[0] == sorted_tokens2[0]:
#        # The first words match, apply token_sort_ratio
#        return fuzz.token_sort_ratio(stringa1.lower(), stringa2.lower())
#    else:
#        # The first words do not match, apply ratio
#        return fuzz.ratio(stringa1.lower(), stringa2.lower())
#
#    # Uguale a quella di prima solo che fa l'analisi onsiderando non la prima parola, ma la prima parola senza l'ultimo carattere


def check_fuzzy_match(stringa1, stringa2):
    """Function to compute fuzzy matching between two strings, with higher weight on matching modified first words."""
    # Split the strings into words
    words1 = stringa1.lower().split()
    words2 = stringa2.lower().split()
    # Extract all characters of the first word except the last one
    modified_word1 = words1[0][:-1] if len(words1) > 0 else ""
    modified_word2 = words2[0][:-1] if len(words2) > 0 else ""
    if modified_word1 == modified_word2:
        # The modified first words match, apply ratio
        return fuzz.token_sort_ratio(stringa1.lower(), stringa2.lower())
    else:
        # The modified first words do not match, return 0
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
            # Increment the counter by how many pairs I've rated so far
            i += 1
    return matched_pairs, counter


# Note that matched_pairs is the array returned by list_fuzzy_similarity
def csv_saving(fileName: str, matched_pairs, output_folder_name):
    """Create a csv file with two ingredients matching and score on each row"""
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


def open_txt(input_file_name_: str):
    """Open a txt file to gather all ingredients list"""
    # Create the dataset
    ingredienti = set()
    # counter = 0
    with open(input_file_name_, encoding="utf-8") as file_txt:
        for row in file_txt:
            # Avoid duplicates
            ingredient_name = row.strip()
            if row not in ingredienti:
                ingredienti.add(ingredient_name)
    return sorted(ingredienti)


def main():

    INPUT_FILE_FOLDER_NAME = "cartella_genitori"
    OUTPUT_FILE_FOLDER_NAME = "cartella_matching"
    PLANEAT_INGREDIENTS_FILENAME = "all_planeat_ing.txt"
    DISSAPORE_INGREDIENTS_FILENAME = "all_dissapore_ing.txt"

    os.chdir(INPUT_FILE_FOLDER_NAME)

    ingredienti_planeat = open_txt(PLANEAT_INGREDIENTS_FILENAME)
    ingredienti_dissapore = open_txt(DISSAPORE_INGREDIENTS_FILENAME)

    # Move back to this script folder
    os.chdir("..")

    #   ------------------------- Finito di creare i due array da confrontare, ne stampo le dimensioni a schermo
    print(f"Ho che ingredienti_planeat ha tot elementi   : {len(ingredienti_planeat)}")
    print(
        f"Ho che ingredienti_dissapore ha tot elementi : {len(ingredienti_dissapore)}"
    )
    #   ------------------------- Obtain the fuzzy similarity
    # Get the list with all the similarities I wanted, with a minimum similarity value equal to 83
    complete_similarity_list, ingr_match_counter = list_fuzzy_similarity(
        ingredienti_planeat, ingredienti_dissapore, 70
    )

    print(
        f"Sono state trovate tot corrispondenze : {ingr_match_counter} con una soglia pari a : ... "
    )
    print("Inizio salvataggio file complete_similarity_list")

    csv_saving(
        "complete_fuzzy2B.csv",
        complete_similarity_list,
        OUTPUT_FILE_FOLDER_NAME,
    )


# Need to add this
if __name__ == "__main__":
    main()
