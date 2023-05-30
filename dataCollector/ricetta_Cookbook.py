# This class have been used inside dataCollector.py
# In the next program, dataCollector2. we would use the other ricettaNew
class info_recipe:
    def __init__(
        self,
        title,
        description,
        instructions,
        ingredients,
        portions,
        details,
        acquisition_time,
        link,
        portata_name,
    ):
        self.title = title
        self.description = description
        self.instructions = instructions
        self.ingredients = ingredients
        self.portions = portions
        self.details = details
        self.acquisition_time = acquisition_time
        self.link = link
        self.portata_name = portata_name

    # Define the function that transform a recipe in a dictionary
    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "instructions": self.instructions,
            "ingredients": self.ingredients,
            "portions": self.portions,
            "details": self.details,
            "acquisition time": self.acquisition_time,
            "link": self.link,
            "portata_name": self.portata_name,
        }
