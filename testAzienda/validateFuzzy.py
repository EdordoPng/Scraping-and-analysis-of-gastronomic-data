import pandas as pd
import os

# ENG :

# Program that:
#    - Selects 1000 rows from the complete fuzzy file threshold 1
#           Note that it is necessary to randomly select 200 matches and 800 non-matches
#    - Sets a column that will be manually filled with 1s and 0s depending on whether they match or not

# ITA :

# Programma che :
#    - Seleziona 1000 righe dal file complete fuzzy soglia 1
#           Nota che serve andare a prendere casualmente 200 che matchano e 800 che non matchano
#    - Vado a settare una colonna che andrò a riempire manualmente con 1 e 0 in base a che matchino o no


def collect_row_samples():
    """Collect a subset of 1000 rows from the complete matching between our ingredients dataset and the one from dissapore"""
    os.chdir("cartella_matching")
    # Set a variable for the requested quantity
    REQUESTED_ROW_QUANTITY = 1000

    df = pd.read_csv("complete_fuzzy_soglia_1.csv")

    df = df.rename(columns={"Indice di Fuzzy": "Match Value"})
    df = df.rename(columns={"Ingrediente Lista 1": "Ingrediente Planeat"})
    df = df.rename(columns={"Ingrediente Lista 2": "Ingrediente Dissapore"})

    sampled_df = pd.DataFrame()
    for i in range(10):
        lower_range = i * 10
        upper_range = (i + 1) * 10
        range_df = df[
            (df["Match Value"] >= lower_range) & (df["Match Value"] < upper_range)
        ]
        print(
            f"Numero di righe con Match Value tra {lower_range} e {upper_range}: {len(range_df)}"
        )
        range_sample = range_df.sample(n=int(REQUESTED_ROW_QUANTITY / 10), replace=True)
        sampled_df = sampled_df.append(range_sample)

    # Sample the remaining rows randomly from the entire dataframe
    remaining_rows = REQUESTED_ROW_QUANTITY - len(sampled_df)
    if remaining_rows > 0:
        remaining_sample = df.sample(n=remaining_rows, replace=True)
        sampled_df = sampled_df.append(remaining_sample)

    # Set the value of the 'Match Value' column to zero in the sampled rows
    sampled_df.loc[:, "Match Value"] = 0

    print(sampled_df.to_string(index=False))
    os.chdir("..")

    sampled_df.to_csv("saggio_1000_righe_fuzzy.csv", index=False)


def open_campioni():
    df = pd.read_csv("campione_1000_righe.csv")


def main():
    # Call this function to create the saggio_1000_righe_fuzzy csv file that contains 1000 row samples
    collect_row_samples()

    open_campioni()


# Need to add this
if __name__ == "__main__":
    main()
