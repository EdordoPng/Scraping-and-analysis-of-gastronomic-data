class info_ricetta_monoporzione:
    # This counter take trace on how much of number of ingredient we don't have to create the recipe
    counter = 0

    def __init__(
        self,
        title,
        description,
        instructions,
        ingredients,
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
    ):
        self.title = title
        self.description = description
        self.instructions = instructions
        self.ingredients = ingredients
        self.kcal = kcal
        self.country_cook = country_cook
        self.difficulty = difficulty
        self.cook_time = cook_time
        self.preparation_time = preparation_time
        self.glutenfree = glutenfree
        self.lactosefree = lactosefree
        self.vegetarian = vegetarian
        self.acquisition_time = acquisition_time
        self.link = link
        self.portata_name = portata_name

    # Function to transform the recipe in a dictionary
    def to_dict(self):
        return {
            "Titolo": self.title,
            "Descrizione": self.description,
            "Istruzioni": self.instructions,
            "Ingredienti": self.ingredients,
            "Kcal": self.kcal,
            "Cucina": self.country_cook,
            "Difficoltà": self.difficulty,
            "Tempo Cottura": self.cook_time,
            "Tempo Preparazione": self.preparation_time,
            "Senza Glutine": self.glutenfree,
            "Senza Lattosio": self.lactosefree,
            "Vegetariano": self.vegetarian,
            "Data Acquisizione": self.acquisition_time,
            "Link": self.link,
            "Portata di appartenenza": self.portata_name,
        }

    # Set metod for the intern contator
    def set_counter_ingredienti_mancanti(self, valore: int):
        self.counter = valore

    # Get metod for the intern contator
    def get_counter_ingredienti_mancanti(self):
        return self.counter
