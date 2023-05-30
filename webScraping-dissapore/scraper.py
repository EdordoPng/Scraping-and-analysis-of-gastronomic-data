import json
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import logging

# This program defines a function that takes the Portata name and web scrape the information found at the target website
# There is also an optional parameter that manage the time between scraping two different recipes


def manage_sleep(tempo_sleep: int):
    """This function manipulates the sleeping time."""
    # Default value of 3 seconds to wait between opening a recip link and the next one
    sleep_time = 3
    if tempo_sleep >= 1:
        sleep_time = tempo_sleep
    return sleep_time


def setup_logger(
    name,
    log_file,
    formatter=logging.Formatter("%(asctime)s %(levelname)s %(message)s"),
    level=logging.DEBUG,
):
    """
    Function to setup a generic loggers.

    :param name: name of the logger
    :type name: str
    :param log_file: file of the log
    :type log_file: str
    :param formatter: formatter to be used by the logger
    :type formatter: logging.Formatter
    :param level: level to display
    :type level: int
    :return: the logger
    :rtype: logging.Logger
    """
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


def scraping(url: str, nomePortata: str, sleep_time: int):
    """This function produces a json file with the Portata name."""

    # Creation of a Selenium driver to open web browser. Note that like this it will open the web
    # without the GUI (Graphic user interface that let you see what the program does on the web)
    # To see it, remove these three line down, and put this : driver = webdriver.Firefox()
    op = webdriver.FirefoxOptions()
    op.add_argument("--headless")
    driver = webdriver.Firefox(options=op)

    # Initialize the value of the waiting time between a recipe and the next one
    tempo_dormienza = manage_sleep(sleep_time)

    # Create a list to keep recipes information
    recipes = []

    # Create the counter of the page we're analyzing (start from the first page)
    page_count = 1
    # Create the counter of the obtained recipes
    recipe_count = 0

    # Creation and managing of the log file
    scraping_log = setup_logger(
        "log_file",
        "log_file.log",
    )

    # This cycle continues untill he finds no more pages
    while True:
        # Use the url provided in input
        driver.get(url)

        # Wait 10 second ( to wait until web site if fully and correctly opened )
        driver.implicitly_wait(10)

        # Create BeautifulSoup for website analysis
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find all <div> that conteins recipe informations
        recipe_divs = soup.find_all("div", class_="card border-0 mb-4")

        # Print on the log file the page that we're analyzing
        scraping_log.info(f"Pagina : {page_count}")

        # For every <div> that conteins recipe informations
        for recipe_div in recipe_divs:

            # Find the recipe title
            title = recipe_div.find("h3").text.strip().replace("\n", "")

            # Find recipe link
            link = recipe_div.find("a")["href"]

            # Open recipe link
            driver.get(link)

            # Wait tot second before opening next recipe
            time.sleep(tempo_dormienza)

            # Create a new BeautifulSoup object for recipe page analysis
            recipe_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Find details (like cook time , portions ...)
            # Used the rec variablke to check if what has been found by the find method is not None to prevent error
            rec = recipe_soup.find(
                "div",
                class_="col-12 col-md-4 mr-md-3 mr-lg-5 mb-3 p-3 recipe-panel-info",
            )
            if rec is not None:
                details = rec.text.strip().replace("\n", "")
            else:
                # else if the detail section isn't been found, just discard the recipe and print the message to the log file

                # Adding the recipe sentence to the log file
                scraping_log.info(
                    f"La {recipe_count + 1} : {title}, della portata {nomePortata}, viene scartata perhè non valida"
                )
                # Doing this, the recipe will be discarded
                continue

            # Find recipe description
            section = recipe_soup.find("section", class_="article__body pb-4")

            # The recursive=False parameter means to find only <p> tag that aren't self contained in other <div> tag
            paragraphs = section.find_all("p", recursive=False)

            description = ""
            for p in paragraphs:
                description += p.get_text()

            # Find the step to make the recipe
            instructions = ""

            # Search all <div> tag with class_ = "step-text"
            step_text_divs = section.find_all("div", class_="step-text")

            # For every <div> with  class_ "step-text"
            for step_text_div in step_text_divs:
                # Take all <p>
                paragraphs = step_text_div.find_all("p")
                # Append text contained inside all <p> to instruction string
                for p in paragraphs:
                    instructions += p.get_text()

            # Take a snapshot on last time when this recipe was actually fine scraped
            acquisition_time = time.strftime("%d/%m/%Y %H:%M:%S")

            # Find ingredients list
            ingredients_list = recipe_soup.find_all("ul", id="lista_ingredienti")

            # Create a list to keep recipe ingredients
            ingredients = []

            # Used numeroLista to resolve the problem of having more ingredient list, like for pasta of the inside of the dish
            for numeroLista in ingredients_list:

                # For every element in the ingredient list
                for ingredient_li in numeroLista.find_all("li", class_="mb-1"):
                    # Find ingredient name
                    ingredient_name = ingredient_li.find(
                        "span", class_="font-weight-bold"
                    ).text
                    ingredient_name = ingredient_name.strip().replace("\n", "")
                    # Find ingredient quantity
                    ingredient_amount = (
                        ingredient_li.find("span", class_="font-weight-bold")
                        .find_next_sibling("span")
                        .text
                    )
                    ingredient_amount = ingredient_amount.strip().replace("\n", "")

                    # Add ingredient to the list
                    ingredients.append(
                        {"name": ingredient_name.lower(), "amount": ingredient_amount}
                    )
            # Update the obtained recipe count :
            recipe_count = recipe_count + 1

            # Adding the recipe sentence to the log file
            scraping_log.info(f"{recipe_count} ricette {nomePortata} ottenute")

            # Add what we took
            recipes.append(
                {
                    "title": title,
                    "description": description,
                    "instructions": instructions,
                    "ingredients": ingredients,
                    "details": details,
                    "acquisition time": acquisition_time,
                    "link": link,
                }
            )
        # Find the <a> tag that conteins the next page link
        next_link = soup.find("a", class_="next")

        # If the <a> tax exists, then there is la following page then set the link in the url variable
        if next_link:
            url = next_link["href"]
            # Grow by 1 the value of the page we're analyzing
            page_count = page_count + 1
        else:
            # Print on the log file the last page and a message to assert the work is fully done
            scraping_log.info(
                f"{page_count} is the last one page. Creating the json file for {nomePortata}"
            )
            # Print the message also on the terminal
            print(
                f"{page_count} is the last one page. Creating the json file for {nomePortata}"
            )
            # If the <a> tag does not exists, we came to the last page
            break

    # ------------------------ folder_name folder creation ------------------------
    # Define the folder name to store the JSON file, then
    folder_name = "cartella_portate"

    # With this instruction we move to work into the mother folder, because I need to create the folder_name folder
    # to contain all the json files extracted, one for each Portata
    os.chdir("..")

    # Check if the folder exists, if not create the folder cartella_portate
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # ----------------------- "PortataName".json file creation ----------------------
    filename = nomePortata + ".json"
    file_path = os.path.join(folder_name, filename)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(recipes, file, ensure_ascii=False, indent=2)
    print(f"File JSON : {file_path} has been succesfully created.")

    # Print inside mylog.log the time stamp of the time when we correctly complete the scraping
    # log_correct_use.info("Date e Time of last correct execution")
    scraping_log.info("Date e Time of last correct execution")
    # Closing Selenium Driver
    driver.close()
