from sklearn.metrics import confusion_matrix
import pandas as pd
import completeFuzzy as cf1
import completeFuzzy2 as cf2
import completeFuzzy2B as cf2B
import completeFuzzy3 as cf3
import completeFuzzy4 as cf4
import completeFuzzy5 as cf5
import completeFuzzy6 as cf6

# ENG :

# This program tests how much correct respones we get when analyzing the campione_1000_righe.csv, wich contains 1000
# recipe couples, and a number that means if there is a correlation or not. 1 if correlation, 0 else.
# We get this value and compare it with the response we get into various cf1 ... cf6 methods, defined in different ways
# We try to get the best performer.
# This program works using the confusion matrix.

# ITA :

# Nota che campione_1000_rows è composto da 1000 coppie di ingredienti e, sulla terza colonna, il loro coefficiente di similarità,
# che sarà posto a 1 se vi è correlazione, 0 altrimenti.
# Questo programma controlla quante risposte corrette otteniamo analizzando validation_set.csv
# Otteniamo questo valore e lo confrontiamo con la risposta che otteniamo in vari metodi cf1 ... cf6, definiti in modi diversi
# Cerchiamo di ottenere le migliori prestazioni.
# Questo programma funziona utilizzando la matrice di confusione.

# We calulate via the confusion matrix:
#       - True Negative
#       - False Positive,
#       - False Negative,
#       - True Positive
#       - Precision
#       - Speificity
#       - Recall
#       - F1_score
# In the end, we print these thing on terminal.

# Valore e soglia con cui confrontarlo
def get_binary_value(value: int, theshold: int):
    """Obtain a binary number based on if the input value is greater than the theshold"""
    if value >= theshold:
        return 1
    else:
        return 0


# Note that matched_pairs is the array returned by list_fuzzy_similarity
def file_saving(risultati):
    """Create a csv file with fuzzy test evaluation statistics"""
    # Write the matched pairs to a CSV file
    df_risultati = pd.DataFrame(risultati)
    df_risultati["Versione"] = df_risultati["Versione"].astype(str)

    # Add results to dictionary
    df_risultati["Soglia"] = df_risultati["Soglia"].astype(int)
    df_risultati["Risposte Corrette"] = df_risultati["Risposte Corrette"].astype(int)
    df_risultati["Risposte Incorrette"] = df_risultati["Risposte Incorrette"].astype(
        int
    )
    df_risultati["True Positive"] = df_risultati["True Positive"].astype(int)
    df_risultati["True Negative"] = df_risultati["True Negative"].astype(int)
    df_risultati["False Positive"] = df_risultati["False Positive"].astype(int)
    df_risultati["False Negative"] = df_risultati["False Negative"].astype(int)
    df_risultati["Precisione"] = df_risultati["Precisione"].astype(float)
    df_risultati["Specificità"] = df_risultati["Specificità"].astype(float)
    df_risultati["Recall"] = df_risultati["Recall"].astype(float)
    df_risultati["F1 Score"] = df_risultati["F1 Score"].astype(float)

    # Save a csv file and an excel one with the obtained datas
    df_risultati.to_csv("testFuzzy.csv", index=False)
    df_risultati.to_excel("testFuzzy.xlsx", index=False)


def convert_score_cf1(
    planeat_ingredient: str, dissapore_ingredient: str, theshold: int
):
    """Convert the int number in range from 0 to 100 into a binary value based on theshold value in input"""
    # Obtain score using the imported function
    score = cf1.check_fuzzy_match(planeat_ingredient, dissapore_ingredient)
    # Convert score to binary value based on theshold value
    binary_score = get_binary_value(score, theshold)
    return binary_score


def convert_score_cf2(
    planeat_ingredient: str, dissapore_ingredient: str, theshold: int
):
    """Convert the int number in range from 0 to 100 into a binary value based on theshold value in input"""
    # Obtain score using the imported function
    score = cf2.check_fuzzy_match(planeat_ingredient, dissapore_ingredient)
    # Convert score to binary value based on theshold value
    binary_score = get_binary_value(score, theshold)
    return binary_score


def convert_score_cf2B(
    planeat_ingredient: str, dissapore_ingredient: str, theshold: int
):
    """Convert the int number in range from 0 to 100 into a binary value based on theshold value in input"""
    # Obtain score using the imported function
    score = cf2B.check_fuzzy_match(planeat_ingredient, dissapore_ingredient)
    # Convert score to binary value based on theshold value
    binary_score = get_binary_value(score, theshold)
    return binary_score


def convert_score_cf3(
    planeat_ingredient: str, dissapore_ingredient: str, theshold: int
):
    """Convert the int number in range from 0 to 100 into a binary value based on theshold value in input"""
    # Obtain score using the imported function
    score = cf3.check_fuzzy_match(planeat_ingredient, dissapore_ingredient)
    # Convert score to binary value based on theshold value
    binary_score = get_binary_value(score, theshold)
    return binary_score


def convert_score_cf4(
    planeat_ingredient: str, dissapore_ingredient: str, theshold: int
):
    """Convert the int number in range from 0 to 100 into a binary value based on theshold value in input"""
    # Obtain score using the imported function
    score = cf4.check_fuzzy_match(planeat_ingredient, dissapore_ingredient)
    # Convert score to binary value based on theshold value
    binary_score = get_binary_value(score, theshold)
    return binary_score


def convert_score_cf5(
    planeat_ingredient: str, dissapore_ingredient: str, theshold: int
):
    """Convert the int number in range from 0 to 100 into a binary value based on theshold value in input"""
    # Obtain score using the imported function
    score = cf5.check_fuzzy_match(planeat_ingredient, dissapore_ingredient)
    # Convert score to binary value based on theshold value
    binary_score = get_binary_value(score, theshold)
    return binary_score


def convert_score_cf6(
    planeat_ingredient: str, dissapore_ingredient: str, theshold: int
):
    """Convert the int number in range from 0 to 100 into a binary value based on theshold value in input"""
    # Obtain score using the imported function
    score = cf6.check_fuzzy_match(planeat_ingredient, dissapore_ingredient)
    # Convert score to binary value based on theshold value
    binary_score = get_binary_value(score, theshold)
    return binary_score


def check_version(
    version: str, planeat_ingredient: str, dissapore_ingredient: str, theshold: int
):
    # Check version name to decide wich function to call
    score = 0
    if version == "cf1":
        score = convert_score_cf1(planeat_ingredient, dissapore_ingredient, theshold)
    elif version == "cf2":
        score = convert_score_cf2(planeat_ingredient, dissapore_ingredient, theshold)
    elif version == "cf2B":
        score = convert_score_cf2B(planeat_ingredient, dissapore_ingredient, theshold)
    elif version == "cf3":
        score = convert_score_cf3(planeat_ingredient, dissapore_ingredient, theshold)
    elif version == "cf4":
        score = convert_score_cf4(planeat_ingredient, dissapore_ingredient, theshold)
    elif version == "cf5":
        score = convert_score_cf5(planeat_ingredient, dissapore_ingredient, theshold)
    elif version == "cf6":
        score = convert_score_cf6(planeat_ingredient, dissapore_ingredient, theshold)
    else:
        print("Version name not found")
        SystemExit
    return score


def get_response(df_risposte, soglia, version, risultati):

    APPROSSIMATION_VALUE = 3
    correct_counter = 0
    incorrect_counter = 0

    y_true = df_risposte["Match Value"].values
    y_pred = []
    # Iterate along dataframe rows and access columns
    for index, row in df_risposte.iterrows():
        ingrediente_planeat = row["Ingrediente Planeat"]
        ingrediente_dissapore = row["Ingrediente Dissapore"]
        # Get the match value, it is a binary value that says if there is similarity between the two ingredients or not
        # Use this value as a truthful answer with which to compare the outcome of my parsing functions
        match_value = row["Match Value"]

        score = check_version(
            version, ingrediente_planeat, ingrediente_dissapore, soglia
        )
        y_pred.append(score)
        # Check if values are the same
        if score == match_value:
            correct_counter = correct_counter + 1
        else:
            incorrect_counter = incorrect_counter + 1

    true_negative, false_positive, false_negative, true_positive = confusion_matrix(
        y_true, y_pred
    ).ravel()
    # Precisione o sensibilità
    if true_positive + false_positive != 0:
        precision = true_positive / (true_positive + false_positive)
    else:
        precision = 0
    precision = round(precision, APPROSSIMATION_VALUE)

    # Speificità
    speificity = true_negative / (true_negative + false_negative)
    speificity = round(speificity, APPROSSIMATION_VALUE)

    # Recall
    recall = true_positive / (true_positive + false_negative)
    recall = round(recall, APPROSSIMATION_VALUE)

    # f1 score è quindi definito come la media armonica tra precisione e richiamo
    if precision + recall != 0:
        f1_score = 2 * precision * recall / (precision + recall)
    else:
        f1_score = 0
    f1_score = round(f1_score, APPROSSIMATION_VALUE)

    # Delete wrost performances
    if correct_counter > 800 and f1_score > 0.8:

        # Add results to dictionary
        risultati["Versione"].append(version)
        risultati["Soglia"].append(soglia)
        risultati["Risposte Corrette"].append(correct_counter)
        risultati["Risposte Incorrette"].append(incorrect_counter)
        risultati["True Positive"].append(true_positive)
        risultati["True Negative"].append(true_negative)
        risultati["False Positive"].append(false_positive)
        risultati["False Negative"].append(false_negative)
        risultati["Precisione"].append(precision)
        risultati["Specificità"].append(speificity)
        risultati["Recall"].append(recall)
        risultati["F1 Score"].append(f1_score)


def get_version_response(df, version):
    risultati = {
        "Versione": [],
        "Soglia": [],
        "Risposte Corrette": [],
        "Risposte Incorrette": [],
        "True Positive": [],
        "True Negative": [],
        "False Positive": [],
        "False Negative": [],
        "Precisione": [],
        "Specificità": [],
        "Recall": [],
        "F1 Score": [],
    }

    for versione in version:
        # This line creates a for loop that goes from 0 to 100 (inclusive), stepping by 10 on each iteration.
        # This means that the loop iterates over 10 values ​​(10, 20, ..., 100).
        for soglia in range(10, 101, 10):
            get_response(df, soglia, versione, risultati)
    # risultati.astype(int).groupby
    file_saving(risultati)


def main():

    VERSIONI = ["cf1", "cf2", "cf2B", "cf3", "cf4", "cf5", "cf6"]

    df = pd.read_csv("validation_set.csv")

    get_version_response(df, VERSIONI)


# Need to add this
if __name__ == "__main__":
    main()
