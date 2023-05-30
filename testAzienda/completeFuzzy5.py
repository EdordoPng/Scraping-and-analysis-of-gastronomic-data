# Questo programma vuole unire fuzzy 3 e 4, in modo tale da avere un programma che assegna un contributo
# che è in parte : moltiplicativo, additivo, standard (standard prevede il confronto fuzzy similarity normale)

import re
import csv
from fuzzywuzzy import fuzz
import datetime
import os

# Questo programma mi fornisce già un fuzzy più attento e complesso in quanto ha sia un contributo additivo che moltipliativo

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
def check_fuzzy_match(stringa1, stringa2):
    """Function to compute fuzzy matching between two strings."""
    # Ingredienti presenti in Dissapore ma non in Planeat
    ingredienti_da_non_considerare = {
        "maiale",
    }
    # Parole che sporcano soltanto la mia ricerca di matching
    parole_da_rimuovere = {
        "di",
        "a",
        "in",
        "con",
        "per",
        "da",
        "tritato",
        "tocchetti",
        "surgelati",
        "fresco",
        "fresca",
        "freschi",
        "grattugiato",
        "fiocchi",
        "prezzemolate",
        "grattugiata",
        "macinato",
        "macinata",
        "salamoia",
        "stagionato",
        "integrale",
        "precotta",
        "ciliegini",
        "datterini",
        "cubettato",
        "affettato",
        "quarto",
        "passata",
        "bio",
        "evo",
        "fresco",
        "fresche",
        "intero",
        "taglio",
        "tagliato",
        "scaglie",
        "fette",
        "fettine",
        "dadini",
        "macinato",
    }
    # Se ingredienti ha nel nome una parola che india un ingrediente da non considerare, il legame tra gli ingredienti in input è 0
    for i in ingredienti_da_non_considerare:
        if i in stringa1.lower() or i in stringa2.lower():
            return 0

    # Vado ad eliminare le parentesi ed il testo contenuto al loro interno, qualora presenti
    stringa1_no_parentesis = re.sub(r"\([^()]*\)", "", stringa1)
    stringa2_no_parentesis = re.sub(r"\([^()]*\)", "", stringa2)

    # Split the two strings into their respective words
    words1 = stringa1_no_parentesis.lower().split(",")
    words2 = stringa2_no_parentesis.lower().split(",")
    # Check if the first words of the two strings are the same

    score = fuzz.ratio(stringa1_no_parentesis.lower(), stringa2_no_parentesis.lower())
    # Controlla se le prime parole dei due ingredienti sono uguali, o se una è parte dell0altra e vieversa
    if (
        words1[0][:-1] == words2[0][:-1]
        or words1[0][:-1] in words2[0][:-1]
        or words2[0][:-1] in words1[0][:-1]
    ):

        # Vedo se ci sono delle sottostringhe in comune, forse meglio mettere questo controllo come esterno al check
        # sulla prima parola
        # Non volgio lavorare con le parole che hanno già un matching perfetto, o che son composte da 4 parole
        # Questa cosa è opinabile, fare ragionamento mais e maiale
        if score != 100 and len(words1[0][:-1]) > 3 and len(words2[0][:-1]) > 3:

            # Converti le stringhe in set di sottostringhe
            sottostringhe1 = set(stringa1_no_parentesis.split())
            sottostringhe2 = set(stringa2_no_parentesis.split())

            sottostringhe1_senza_parole = sottostringhe1 - parole_da_rimuovere
            sottostringhe2_senza_parole = sottostringhe2 - parole_da_rimuovere
            # Ottengo le parole comuni ad entrambi gli ingredienti
            comuni = sottostringhe1.intersection(sottostringhe2)

            if (
                len(comuni)
                >= (len(sottostringhe1_senza_parole) + len(sottostringhe2_senza_parole))
                / 2
            ):
                # Se vero, allora ho che almeno la metà delle parole sono in comune ad i due ingredienti
                # Anche se forse è poco accurato in quanto può essere che il primo ingrediente ha una sola parola ed il seondo ne ha 7
                # quindi i sarebbe da aggiustare qualcosa qui
                score *= 2
            # Increase the score by 10% if the two strings have the same first word without the last letter
            # if words1[0][:-1] == words2[0][:-1] or words1[0][:-1] in words2[0][:-1]:

            score = score + 30
        # Se ho dei punteggi piu grandi di 100 a causa delle varie manipolazioni, setto il valore a 99
        # if score > 100:
        #    score = 99
        return round(score)
    # Se son si verifica he i due ingredienti abbiano la prima parola (privata dell'ultima lettera ) uguale, o che
    else:
        if (
            len(stringa1_no_parentesis.lower()) == 1
            and len(stringa2_no_parentesis.lower()) == 1
            and stringa1_no_parentesis.lower() not in stringa2_no_parentesis.lower()
        ):
            score *= 0.5
        score *= 0.8
        return round(score)


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
    SOGLIA = 55
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
    # Get the list with all the similarities I wanted, with a minimum similarity value equal to 52
    complete_similarity_list, ingr_match_counter = list_fuzzy_similarity(
        ingredienti_planeat, ingredienti_dissapore, SOGLIA
    )

    print(
        f"Sono state trovate tot corrispondenze : {ingr_match_counter} con una soglia pari a : {SOGLIA} "
    )
    print("Inizio salvataggio file complete_similarity_list")

    csv_saving(
        "complete_fuzzy5.csv",
        complete_similarity_list,
        OUTPUT_FILE_FOLDER_NAME,
    )


# Need to add this
if __name__ == "__main__":
    main()
