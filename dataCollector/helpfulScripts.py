# These import would be needed inside estraiQuantita
import re
from fractions import Fraction

# ENG : 

# Useful program to correctly extract the serving number contained in the "detail"argoment passed in input. 
# This would be imported into dataCollector to be used. 

# ITA :

# Programma utile per estrarre correttamente il numero della porzione contenuto nell'argomento "detail" passato in input.
# Questo verrebbe importato in Data Collector per essere utilizzato.

porzioni = 0
# This function lets you estrapolate the serving number that could be make with the requested ingredients
def ricercaNumeroPortate(dettagliRicetta: str):
    # Check if the word "Person" is found inside details string, if not then we doesn't know the number of serving
    # cause data missing. We set it to 1 to not leave the field empty. Note, we get -1 if the word Person is not found
    if dettagliRicetta.find("Person") == -1:
        return 1
    else:
        # Managing string to extract the serving number
        lista = dettagliRicetta.split("Porzioni:")
        lista1 = lista[1].split("Person")
        lista2 = lista1[0]
        lista3 = lista2.replace(" ", "")
        porzioni = int(lista3)
        return porzioni


# Need to manage input datas that came in form of string. Serving number needs to be casted to int type

# Es. input string : "300 g" oppure "1 Cucchiaio" oppure "2 Rametto" oppure "1 Mazzetto" oppure "1 Pizzico"
def estrai_quantita(stringa: str):
    # Use this regular expression to extract the number at the string beginning
    # This regular expression search for a number, maybe followed by a dot and another number, or a slash / and another number.
    # In this way we can extract the elemnets in the correct way
    pattern = r"^\d+(\.\d+)?(/\d+)?"
    # Search for the pattern into the input string,
    risultato = re.search(pattern, stringa)

    if risultato is None:
        # If he doesn't find any number, return 0.
        # In this way even when on website there isn't a set number, I put 0 and then in dataCollector.py we
        # set it to "q.b." (quanto basta)
        return 0
    else:
        # If finds a number, check for the 1/2 notation
        numero = risultato.group()
        if "/" in numero:
            # If contains that expression, convert the expression in a float number
            numero_decimale = float(Fraction(numero))
        else:
            # Altrought, convert the number directly to float
            numero_decimale = float(numero)
        return numero_decimale


# This function takes in input the ingredient's requeste quantity. Then it need to be divided by the serving number
# to obtain the right weight for the mono serving recpie
def divisorePorzioni(stringaQuantita: str, numeroPorzioni: int):
    valore = estrai_quantita(stringaQuantita)
    if valore == None:
        return None
    result = round(valore / numeroPorzioni, 3)
    return int(result) if result.is_integer() else result


# This function takes in input the ingredient's requeste quantity, it is in a format like 300g o 300 ml o 1/2.
# It's used to extract the ingredient unit of measure
def estrai_unita_misura(stringaQuantita: str):
    # Use this regular expression to extract the number at the string beginning
    pattern = r"^\d+(\.\d+)?(/\d+)?"
    # Search for the pattern into the input string,
    risultato = re.search(pattern, stringaQuantita)
    if risultato is None:
        # If a number isn't found, return an empty string
        return ""
    else:
        # If a number isn't found,, collect the first char index
        indice_inizio_numero = risultato.start()
        # Obtain the unit of measure extracting the substring starting by the index next to the number
        unita_misura = stringaQuantita[indice_inizio_numero + len(risultato.group()) :]
        # Remove the starting and final blanks by the unit of measure
        unita_misura = unita_misura.strip()
        return unita_misura
