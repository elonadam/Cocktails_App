
# TODO 6 to make my closet with my alchol and then new attribute to each cocktail, which alcogol is needed "vodka,gin"
# TODO 7 function that look what you have and suggest by that cocktials

from cocktail_Manager import CocktailManager
from category_manager import CategoryManager
from cocktail import Cocktail
from gui import CocktailAppGUI
manager = CocktailManager("cocktail_book.json")
manager.calculate_and_update_abv()
#
# manager = CocktailManager()
#
cocktaill = Cocktail #delete later
if __name__ == "__main__":
    manager = CocktailManager()  # Handles recipes
    app = CocktailAppGUI(manager)  # Starts the GUI
    category_manager = CategoryManager(manager)

    print(manager.extract_cocktail_names())
