import json
import helpfulScripts
import ricetta_Cookbook
import ricetta_Cookbook_SingleServing
import os
import sys
import argparse
import configparser

# ENG : 

# This program takes all files relatives to Portatas and join them in a final json file named Cookbook.
# Then we extract and put in Cookbook_Monoserving the monoserving maked recipes

# ITA : 
# Questo programma prende tutti i file relativi alle diverse portate e li unisce in un file json finale chiamato Cookbook.
# Quindi estraiamo e inseriamo in Cookbook_Monoserving le ricette realizzate nel caso monoporzione (per 1 persona)

# Definition of a function to correctly take the input by keyboard
def init_argparser():
    """Initialize the command line parser."""
    try:
        parser = argparse.ArgumentParser(
            description="This program collects datas form files in parsed folder and creates 2 new json"
        )
        parser.add_argument(
            "Folder_Name",
            action="store",
            type=str,
            help="Portata's folder name, it contains all Portata's json you want to analyze",
        )
    # If we don't pass anything from keyboard when executing this program, this code will be executed
    except:
        print("La cartella ricercata dovrebbe avere il nome : cartella_portate")
        sys.exit("Riesegui il programma")

    return parser


# Function to check the content of to_skip.conf that contains a list of files to be skipped into the
# dataCollector analysis. It is updatable by user. If the file doesn't exists, it would be created one.
# Note that to_skip isn't in this sript folder, but in the one with all the json.
# So to correctly call this function, before calling it I need to moved inside the cartella_portate already
def setup_json_to_skip():
    """Obtain usefoul datas form the to_skip.ini file."""
    config = configparser.ConfigParser()
    # If the conf file isn't been found, then create a new one
    if not os.path.isfile("to_skip.conf"):
        config["FILES TO SKIP"] = {
            "file1": "to_skip.conf",
            "file2": "Cookbook.json",
            "file3": "Cookbook_SingleServing.json",
        }
        with open("to_skip.conf", "w") as configfile:
            config.write(configfile)
            return [
                "to_skip.conf",
                "Cookbook.json",
                "Cookbook_SingleServing.json",
            ]
    # If the conf is found, then take from there files names of the onbe to be skipped
    else:
        config.read("to_skip.conf")
        json_to_skip = []
        for key in config["FILES TO SKIP"]:
            json_to_skip.append(config["FILES TO SKIP"][key])
        print(
            f' I seguenti file, se presenti in "cartella_portate" verranno scartati. Nomi : {json_to_skip}'
        )
        return json_to_skip


def main():

    # Initialize the parser to manage keyboard input
    parser = init_argparser()
    args = parser.parse_args()

    # Define the folder name where json files are
    folder_name = str(args.Folder_Name)

    # With this instruction we move to work into the mother folder, because I need to search the folder_name folder
    # that contains all the json files extracted, one for each Portata
    os.chdir("..")

    # Check if the folder exists, if not terminate the program with error
    if not os.path.exists(folder_name):
        sys.exit("Files folder was not located inside of this folder : " + os.getcwd())

    # We're working with the mother folder of the one that contains this script. But I want to access the folder_name folder,
    # that contains all json files I want to utilize. moving into folder_name
    os.chdir(folder_name)

    # Run the method to obtain json files that needs to be skipped, put them into a variable. This instruction was put here and
    # and not before due to the needing to work inside the cartella_portate folder to read the to_skip file
    json_to_skip = setup_json_to_skip()

    # Define the data array that will contain the name of each file inside the cartella_portate folder
    data = []
    # A list to contain all different recipes coming from different Portatas
    ricette = []
    # ------------------------------------- json upload -----------------------------------------

    for file in os.listdir():
        # If the file name is inside JSON_TO_SKIP, then they need to be skipped
        if file in json_to_skip:
            continue
        else:
            try:
                with open(file, "r", encoding="utf-8-sig") as f:
                    # Data
                    # data.append(json.load(f))
                    data = json.load(f)
                    # Assegna il nome del file corrente a nome_portata
                    nome_portata = file.split(".")[0]
            except:
                print(
                    f"Errore nell'apertura del file: {file}. Riavviare il programma inserendo il file nella cartella cartella_portate "
                )
                print(
                    f"Alternativamente riavviare il programma inserendo il nome del file problematico tra quelli da scartare, in to_skip.conf "
                )
                sys.exit(1)

            print(f"File : {file} has been succesfully identified and used.")

            # -------------------------------- Start script execution ------------------------------------

            for recipe in data:
                # Accessing recipe various datas
                title = recipe["title"]

                # Use this to skip eventually repeated recipes (due to presence in various portatas of a recipe)
                if any(r.to_dict()["title"] == title for r in ricette):
                    continue

                description = recipe["description"]
                instructions = recipe["instructions"]
                ingredients = recipe["ingredients"]
                details = recipe["details"]
                acquisition_time = recipe["acquisition time"]
                link = recipe["link"]
                # Once details collected, now I would like to know the number of serving that will be created with theese ingredients and recipe.

                # Used the ricercaNumeroPortate(str) contained in helpfulScripts.py.
                portions = helpfulScripts.ricercaNumeroPortate(details)
                # Now need to obtain the ingredient list with the respective weight divided by number of serving ( Porzioni )
                # This to obtain the new weight in the mono serving case (1 serving)
                ingredienti = []
                # Iterate throught the ingredients list and add the amount of every ingredient to the list
                for ingredient in ingredients:
                    # This construct need to modify the ingredient quantity cause some of them have it set to 0
                    # Sobstituting it with the string "q.b." It means "Quanto basta"
                    if ingredient["amount"] == 0:
                        ingredienti.append(
                            {
                                "Nome": ingredient["name"].strip().replace("  ", " "),
                                "Quantità": "q.b.",
                                "Unità di misura": "Unita",
                            }
                        )
                    else:
                        # Adding weight and the unit of measure to mono serving ingredients
                        # Then put the ingredient name ad the weight in the mono serving case, then the unit of measure
                        ingredienti.append(
                            {
                                "Nome": ingredient["name"].strip().replace("  ", " "),
                                # Problema perch+ amount è sporco
                                "Quantità": str(
                                    helpfulScripts.estrai_quantita(
                                        str(ingredient["amount"])
                                    )
                                ),
                                # Appending the unit of measure
                                "Unità di misura": helpfulScripts.estrai_unita_misura(
                                    str(ingredient["amount"])
                                ),
                            }
                        )
                # Need to use this cycle to fix unmatching datas in unit of measure and quantity
                for ric in ricette:
                    for ingr in ric.ingredients:
                        # In this way we came to every ingredient
                        if ingr["Unità di misura"] == "":
                            ingr["Unità di misura"] = "Unità"
                        if ingr["Quantità"] == "0":
                            ingr["Quantità"] = "q.b."
                if ingredienti == []:
                    continue
                # Updating the recipe list
                ricette.append(
                    ricetta_Cookbook.info_recipe(
                        title,
                        description,
                        instructions,
                        ingredienti,
                        portions,
                        details,
                        acquisition_time,
                        link,
                        nome_portata,
                    )
                )

    # -------------------------- json output creation -----------------------------
    with open("Cookbook.json", "w", encoding="utf-8") as file:
        ricette_dict = [r.to_dict() for r in ricette]
        json.dump(ricette_dict, file, ensure_ascii=False, indent=2)

    # ------------------------------------- Second file work start ---------------------------------------

    # List of all recipe from all Portatas
    ricette = []

    # Open the recipe file
    with open("Cookbook.json", "r", encoding="utf-8") as json_file:
        db_ricette = json.load(json_file)

    # For every recipe contained inside Cookbook
    for recipe in db_ricette:
        # Extract recipe title
        title = recipe["title"]
        # Extract recipe description
        description = recipe["description"]
        # Extract recipe instructions
        instructions = recipe["instructions"]
        # Extract recipe ingredients datas and put in the ingredients attribute, extract from the Coocbook pesoIngrMonoporzione field
        ingredients = recipe["ingredients"]
        # Extract recipe portions
        portions = recipe["portions"]
        # Extract recipe details
        details = str(recipe["details"])

        acquisition_time = recipe["acquisition time"]
        link = recipe["link"]
        portata_name = recipe["portata_name"]

        # Initialize these variables referred to intolerances
        glutenfree = False
        lactosefree = False
        vegetarian = False
        # ------------------------------------ Start details managing section ----------------------------------

        # For every recipe, analyze the details section composed like this :
        # "Dettagli": "Cucina: Statunitense          Difficoltà: Facile          Cottura: 6 Minuti          Preparazione: 10 Minuti          Porzioni:          4 Persone          Prezzo: Basso          Calorie: 175 KcalSenza glutineSenza lattosioVegetariano"
        # Informations estraction
        if "Cucina: " in details:
            country_cook = details.split("Cucina: ")[1].split(" ")[0]
        if "Difficoltà: " in details:
            difficulty = details.split("Difficoltà: ")[1].split(" ")[0]
        if "Cottura: " in details:
            cook_time = (
                str(details.split("Cottura: ")[1].split(" ")[0])
                + " "
                + str(details.split("Cottura: ")[1].split(" ")[1])
            )
        if "Preparazione: " in details:
            preparation_time = (
                str(details.split("Preparazione: ")[1].split(" ")[0])
                + " "
                + str(details.split("Preparazione: ")[1].split(" ")[1])
            )
        # To obtain the right number in the monoserving case,I need to divide the old kcal count by
        # the serving number (if a recipe has 400 kcal and it is for 4 servings, then it would have 100 Kcal )
        if "Calorie: " in details:
            kcal = int(float(details.split("Calorie: ")[1].split(" ")[0]) / portions)

        if "Senza glutine" in details:
            glutenfree = True
        if "Senza lattosio" in details:
            lactosefree = True
        if "Vegetariano" in details:
            vegetarian = True

        # ----------------------------------- End details managing section ------------------------------------

        # Now need to obtain the ingredient list with the respective weight divided by number of serving ( Porzioni )
        # This to obtain the new weight in the mono serving case (1 serving)
        new_weighted_ingredients = []
        # Iterate throught the ingredients list and add the amount of every ingredient to the list
        for ingredient in ingredients:
            # Check if the quantity is a number, if yes divide the ingr quantity by the servings number
            if ingredient["Quantità"] == "q.b.":
                ingredient_quantity = ingredient["Quantità"]
            else:
                ingredient_quantity = str(
                    helpfulScripts.divisorePorzioni(
                        str(ingredient["Quantità"]), portions
                    )
                )
            # Adding weight and the unit of measure to mono serving ingredients
            # Then put the ingredient name ad the weight in the mono serving case, then the unit of measure
            new_weighted_ingredients.append(
                {
                    "Nome": ingredient["Nome"],
                    "Quantità": ingredient_quantity,
                    # Appending the unit of measure
                    "Unità di misura": ingredient["Unità di misura"],
                }
            )

        ricette.append(
            ricetta_Cookbook_SingleServing.info_ricetta_monoporzione(
                title,
                description,
                instructions,
                new_weighted_ingredients,
                kcal,
                country_cook,
                difficulty,
                cook_time,
                preparation_time,
                glutenfree,
                lactosefree,
                vegetarian,
                acquisition_time,
                link,
                portata_name,
            )
        )

    # -------------------------------------- Output in file json -----------------------------------------
    with open("Cookbook_SingleServing.json", "w", encoding="utf-8") as file:
        ricette_dict = [r.to_dict() for r in ricette]
        json.dump(ricette_dict, file, ensure_ascii=False, indent=2)


# Need to add this
if __name__ == "__main__":
    main()
