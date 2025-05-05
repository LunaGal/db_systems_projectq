from backend_functions import RecipeDBConnection
import configparser

config=configparser.ConfigParser()
config.read('config.ini')

host = config['Database']['host']
user = config['Database']['user']
password = config['Database']['password']
dbname = config['Database']['dbname']

# GLOBAL VARIABLES ---------------------------------------------------------------------
# currentPage should always be in camelcase
currentPage = ""
previousPage = ""

userInput = ""
userInputList = []
userCommand = ""

# REUSABLE FUNCTIONS -------------------------------------------------------------------
def bar():
    print("------------------------------")

def pageTitle(title):
    bar()
    print(title)
    bar()

def commandMessage(commandList):
    print("")
    print("Enter one of the following commands:")
    for i in commandList:
        print(i)
    
    # Takes user input
    userInput = input("> ").strip()
    # Separates userInput into a list
    userInputList = userInput.split()
    userCommand = userInputList[0].toLower() if userInputList else ""

def setPage(newPage):
    global previousPage
    global currentPage

    previousPage = currentPage
    currentPage = newPage

def displayRecipe(name, description, authorName, defaultServings, ingredients, steps, tags):
    bar()
    print(name)
    print("By" + authorName)

    tagsList = ""
    for i in tags:
        tagsList = tagsList + i.toString() + ", "
    tagsList = tagsList[:-2]
    print("Tags: " + tagsList)

    print("Default Servings: " + defaultServings)

    print("")
    print(description)
    print("")

    ingredientsList = ""
    for i in ingredients:
        ingredientsList = ingredientsList + i.toString() + ", "
    ingredientsList = ingredientsList[:-2]
    print("Ingredients: " + ingredientsList)

    print("Allergens: ")

    print("Steps:")
    for i in steps:
        print("number) " + "step")
        
    bar()

# PAGES ---------------------------------------------------------------------------------

# TODO: Fill this out
pageMap = {
    "homepage" : homePage,
    "login" : logIn,
    "createprofile" : createProfile,
    "userprofile" : userProfile,
    "createnewrecipe" : createNewRecipe,
    "myrecipes" : myRecipes,
    "starredrecipes" : starredRecipes,
    "mealplan" : mealPlan,
    "searchrecipes" : searchRecipes,
    "logout" : logOut,
    "singlerecipe" : singleRecipe
}

def template():  # TEMPLATE -------------------------------------------------------------
    # Sets up global variables
    global currentPage

    # Sets up title
    pageTitle("")

    # Sets up all necessary information
    

    # Displays commands available to the user & takes input
    commandMessage()
    
    userInput = input("> ").strip().lower()

    # Turns user input into navigation
    if userInput == "":
        currentPage = ""
    else:
        print("Command not recognized, please try again.")

def homePage():
    # Sets up global variables
    global currentPage

    # Title & relavant information
    pageTitle("Recipe-gram")
    print("Brought to you by The Databagels: Luna Gal, Lina Boughton, & Diya Misra")

    # Displays commands available to the user & takes input
    commandsAllowed = ["LogIn", "CreateProfile"]
    commandMessage(commandsAllowed)


    # Turns user input into navigation (ALL LOWERCASE)
    if userCommand == "login":
        setPage("login")
    elif userCommand == "createprofile":
        setPage("createprofile")
    else:
        print("Command not recognized, please try again.")

def logIn():
    # Sets up global variables
    global currentPage

    # Sets up title
    pageTitle("Log-In")    

    # Displays commands available to the user & takes input
    bar()
    print("Enter your username & password with one space inbetween  ->   <yourusername yourpassword>")
    userInput = input("> ").strip().lower()

    # Turns user input into navigation
    #TODO: Check proper login information
    currentPage = "userProfile"

def createProfile():
    # Sets up global variables
    global currentPage

    # Sets up title
    pageTitle("Create Profile")

    # Displays commands available to the user & takes input
    userInput = "n"
    while userInput != "y":
        bar()
        print("Enter your desired username")
        testusername = input("> ").strip()

        print("Your username is " + testusername + " is this correct? <Y/N>")
        userInput = input("> ").strip().lower()
    print("Hello " + testusername + "!")

    userInput = "n"
    while userInput != "y":
        bar()
        print("Enter your desired password")
        testpassword = input("> ").strip()

        print("Your password is " + testpassword + " is this correct? <Y/N>")
        userInput = input("> ").strip().lower()
    print("Thanks for creating a profile with us!")

    # Turns user input into navigation
    #TODO: Check proper create profile stuffs
    currentPage = "userProfile"

def userProfile():
    # Sets up global variables
    global currentPage

    # Sets up title
    pageTitle(("Profile: " + "Your Name")) #TODO: make it connect to username in database

    # Displays commands available to the user & takes input
    commandMessage()
    print("CreateNewRecipe")
    print("ViewMyRecipes")
    print("ViewStarredRecipes")
    print("ViewMealPlan")
    print("SearchRecipes")
    print("Logout")
    userInput = input("> ").strip().lower()

    # Turns user input into navigation
    if userInput == "createnewrecipe":
        currentPage = "createNewRecipe"
    elif userInput == "viewmyrecipes":
        currentPage = "myRecipes"
    elif userInput == "viewStarredRecipes":
        currentPage = "starredRecipes"
    elif userInput == "viewmealplan":
        currentPage = "mealPlan"
    elif userInput == "searchrecipes":
        currentPage = "searchRecipes"
    elif userInput == "logout":
        currentPage = "logout"
    else:
        print("Command not recognized, please try again.")

def createNewRecipe():   #TODO: Finish the command functionalities
    # Sets up global variables
    global currentPage

    # Sets up title
    pageTitle("Create a New Recipe")

    # Outputs the recipe
    print("name") #TODO: connect all of this to the database
    bar()
    print("Tags: " + "tags")
    print("description")
    bar()
    print("ingredients")
    print("steps")

    # Displays commands available to the user & takes input
    commandMessage()
    print("EditName <name>")
    print("AddTag <tagName>")
    print("RemoveTag <tagName>")
    print("EditDescription <description>")
    print("AddStep <step text>") # Add step (must be at least one)
    print("RemoveStep <step number>")
    print("AddIngredient <ingredient name>") # Add ingredient (must be at least one)
    print("RemoveIngredient <ingredient name>")
    print("ReturnToProfile")
    userInput = input("> ").strip().lower()

    # Turns user input into navigation
    if userInput == "editname":
        currentPage = "" #TODO: Update name in database, etc.
    elif userInput == "returntoprofile":
        currentPage = "userProfile"
    else:
        print("Command not recognized, please try again.")

def myRecipes():
    # Sets up global variables
    global currentPage

    # Sets up title
    pageTitle( "name" + "'s Recipes")

    # Sets up all necessary information
    print("List of my recipes") # Use displayRecipe

    # Displays commands available to the user & takes input
    commandMessage()
    print("DeleteRecipe <recipe name>")
    print("EditRecipe <recipe name>")
    print("StarRecipe <recipe name>")
    print("UnstarRecipe <recipe name>")
    print("AddToMealPlan <recipe name>")
    print("RemoveFromMealPlan <recipe name>")
    userInput = input("> ").strip().lower()

    # Turns user input into navigation
    if userInput == "":
        currentPage = ""
    elif userInput == "":
        currentPage = ""
    else:
        print("Command not recognized, please try again.")

# View my starred recipes
    # Info: A list of the recipes the user has starred (Names & descriptions only!)
    # Actions:
        # Select a recipe to view it in detail (below)
        # Unstar a recipe (below)
        # Add recipe to meal plan (below)
        # Remove recipe from meal plan (below)

def starredRecipes():

def mealPlan():

# View my meal plan
    # Info: a list of the recipes in the user's meal plan (name & servings only)
    # Actions:
        # Select a recipe to view it in detail (below)
        # Star a recipe (below)
        # Unstar a recipe (below)
        # Remove recipe from meal plan (below)
        # Edit servings for a recipe

def searchRecipes():

# Search for other recipes
    # Info: A list of recipes in the database (not including the user's own) (10 at a time, maybe)
    # Actions:
        # Filter by tags, ingredients, or allergens
        # Search for recipes (keywords)

def singleRecipe():

# Select a recipe to view it in detail
    # Info: Name, author, description, tags, ingredients, steps
    # Actions:
        # Delete this recipe (if written by user) (below)
        # Edit this recipe (if written by user) (below)
        # Star this recipe (if not starred) (below)
        # Unstar this recipe (if starred) (below)
        # Add this recipe to meal plan (if not in meal plan) (below)
        # Remove this recipe from meal plan (if in meal plan) (below)
        # Edit servings for this recipe (if in meal plan) (below)

# Delete recipe you've written (any recipe)
    # Info: Are you sure you want to delete? (Yes/No)
    # Actions:
        # Yes (deletes recipe, returns to viewing my recipes)
        # No (returns to previous page)

def deleteRecipe(): # deletes recipes that the user has written
    # Sets up global variables
    global currentPage

    # Sets up all necessary information

    #################################################### TODO!!!!!!!!! FINISH THIS FUNCTION!!!!!!!!!!!!!!!!!!!!

    userInput = ""
    print("Are you sure you want to delete this recipe? <Y/N>") 

    while (userInput != "y" or userInput != "n"):
        userInput = input("> ").strip().lower()
        if userInput == "y":
            print("Recipe deleted!")
            # TODO: Actually delete this recipe (nullify) in database
            currentPage = "myRecipes"
        elif userInput == "n":
            currentPage = "e" # TODO: Previous page
        else:
            print("Command not recognized, please try again.")
        

    # Turns user input into navigation
    if userInput == "":
        currentPage = ""
    else:
        print("Command not recognized, please try again.")

# Edit recipe
    # Info: name, tags, description, steps, ingredients
    # Actions:
        # Edit name
        # Add tag (can be none)
        # Remove tag
        # Add description (if there is none)
        # Edit desription
        # Remove description
        # Add step (must be at least one)
        # Edit step
        # Remove step
        # Add ingredient (must be at least one)
        # Remove ingredient

def starRecipe():
    #TODO: Actually star this recipe in the database
    bar()
    print("Recipe Starred!")
    bar()

def unstarRecipe():
    #TODO: Actually unnstar this recipe in the database
    bar()
    print("Recipe Unstarred!")
    bar()

def addMealPlanRecipe():
    #TODO: Actually add this recipe to the meal plan in the database
    bar()
    print("Added recipe to meal plan!")
    bar()

def removeMealPlanRecipe():
    #TODO: Actually delete this recipe from the meal plan in the database
    bar()
    print("Recipe Removed from meal plan!")
    bar()

# Edit Servings for Recipe (in meal plan)
    # Info: Current servings
    # Actions:
        # Enter new servings

def logout():
    global currentPage
    currentPage = "homePage"

    bar()
    print("Logged-out!")
    bar()

# Now we run everything! ------------------------------------------------------------

# Please use the with ... as block
# It ensures that connection commits everything to the database when the program finishes
def run_app(host=host, user=user, password=password):
    with RecipeDBConnection(host, user, password, dbname) as connection:
        global currentPage
        currentPage = "homePage"

        global pageMap
        while True:
            pageMap[currentPage]()


run_app()