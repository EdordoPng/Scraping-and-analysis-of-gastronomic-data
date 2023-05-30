import scraper
import sys
import argparse
import configparser
import os
import scraper

# This progrm calls the function scraping(link_to_Portata, Portata_name, Sleeping_time)
# that creates a json file with the Portata's name.

# Definition of a function to correctly take the input by keyboard
def init_argparser():
    """Initialize the command line parser."""
    parser = argparse.ArgumentParser(
        prog="scrapingPortata.py",
        description="This program scrapes datas form website link put by user and waits tot seconds between recipes scraping",
    )
    parser.add_argument(
        "string",
        action="store",
        type=str,
        help="Portata's name you want to analyze",
    )

    parser.add_argument(
        "seconds",
        action="store",
        type=int,
        nargs="?",
        help="Time to wait before next recipe scraping, range [1,]",
    )
    return parser


# Created so the user now need only to give the portata's name, and not the entire link
def obtain_portata_link():
    """Obtain portata's link form the portata.conf file."""
    config = configparser.ConfigParser()
    # If the conf file isn't been found, then we don't handle this case
    if not os.path.isfile("portata.conf"):
        sys.exit("Not found the portata.conf file")
    # If the conf is found, then take from there files names of the onbe to be skipped
    else:
        config.read("portata.conf")
        portata_links = []
        for key in config["PORTATA'S LINKS"]:
            portata_links.append(config["PORTATA'S LINKS"][key])
        return portata_links


# Check if the name is a valid one
def is_valide_portata_name(portata_name: str):
    """Check if the portata name inserted by the user is a valid one by checking on the portata.conf"""
    config = configparser.ConfigParser()
    config.read("portata.conf")
    # Array with all portata names
    portata_names = []
    # Fill the array
    for link in config["PORTATA'S LINKS"]:
        portata_names.append(link)
    # Check
    if portata_name not in portata_names:
        return False
    return True


# This function calls obtain_portata_link() and is_valide_portata_name() to obtain the right link
# from the portata.conf file
def get_link(portata_name: str):
    """Obtain requested portata's link from the portata.conf file"""
    # Gather all portatas links into an array
    portata_links = obtain_portata_link()
    # Little check on the rightness of the word
    if is_valide_portata_name(portata_name):
        for link in portata_links:
            if portata_name in link:
                return link
    else:
        sys.exit(
            "Put a valid portata name, check the portata.conf file in this folder to know more about it"
        )


# Definition of the main function that will be called once user run the program
def main():
    # Setup important variables to correctly parse the target link
    parser = init_argparser()
    args = parser.parse_args()

    # Obtain the corrispondent link to the portata name parsed by keyboard
    # Note that this name is inside here : args.string
    portata_link = get_link(args.string)

    # Check if the user has put in input a number that rapresents
    if args.seconds == None:
        wait_time = 3
    else:
        wait_time = args.seconds
    # Parameters are : Portata's Link, Portata's Name, Sleeping Time
    scraper.scraping(portata_link, args.string, wait_time)


# Need to add this
if __name__ == "__main__":
    main()
