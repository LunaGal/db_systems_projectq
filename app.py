# PRIOR TO RUNNING
# Update the password field in config.ini & databaseCreator.py to your password

from backend_functions import RecipeDBConnection
import configparser
import enum
from enum import Enum, auto
import collections
from collections import namedtuple

# Code by Luna (backend stuff, presumably)
config=configparser.ConfigParser()
config.read('config.ini')

host = config['Database']['host']
user = config['Database']['user']
password = config['Database']['password']
dbname = config['Database']['dbname']

# Code by Lina below!

#region GENERIC FUNCTIONS ===========================================================================================

# Prints out a bar
def bar():
    print("---------------------------")

# Prints out a longer, thicker bar
def thickBar():
    print("===================================================================================")

# Takes the page object & prints out the title of the page
def displayTitle(givenPage):
    thickBar()
    print(pageMap[givenPage].displayName)
    bar()

# References the user who is logged in
loggedInUser = ""

#endregion ================================================================================================================

#region PAGES ===============================================================================================================

# The pages in the aplication
# IF YOU ADD A PAGE HERE, ADD IT TO PAGEMAP AS WELL!!
class Page(Enum):
    home = auto()
    userProfile = auto()
    createNewRecipe = auto()
    myRecipes = auto()
    myStarredRecipes = auto()
    myMealPlan = auto()
    searchRecipes = auto()
    editRecipe = auto()

# Stores data specific to each page
# displayName -> the name that displays as the title of the page
# behaviorFunction -> called after displaying the name, stores the specific behavior allowed on that page
pageData = namedtuple('pageData', ['displayName', 'behaviorFunction'])

# Maps each page (the enumeration) to its data
# IF YOU ADD A PAGE HERE, ADD IT TO PAGE(ENUM) AS WELL!!
# To access the currentPage:
    # pageMap[currentPage].displayName
    # pageMap[currentPage].behaviorFunction()
pageMap = "" # We'll create & assign the pageMap at runtime
def createPageMap():
    return {
        Page.home : pageData(displayName = "Welcome to Recipe-gram", behaviorFunction = homePage),
        Page.userProfile : pageData(displayName = "My Profile", behaviorFunction = userProfile),
        Page.createNewRecipe : pageData(displayName = "Create a New Recipe", behaviorFunction = createNewRecipe),
        Page.myRecipes : pageData(displayName = "My Recipes", behaviorFunction = myRecipes),
        Page.myStarredRecipes : pageData(displayName = "My Starred Recipes", behaviorFunction = myStarredRecipes),
        Page.myMealPlan : pageData(displayName = "My Meal Plan", behaviorFunction = myMealPlan),
        Page.searchRecipes : pageData(displayName = "Search for Recipes", behaviorFunction = searchRecipes),
        Page.editRecipe : pageData(displayName = "Edit Recipe", behaviorFunction = editRecipe)
    }

# Tracks our current page, initially set to Page.home
currentPage = Page.home
# Tracks our previous page, initially set to Page.home
previousPage = Page.home

# Updates the currentPage & previousPage
def updatePage(newPage):
    global previousPage
    global currentPage

    previousPage = currentPage
    currentPage = newPage

#endregion ================================================================================================================

#region DISPLAY RECIPE FUNCTION ===========================================================================================

# Takes a recipe as input & displays it in text
def displayRecipe(givenRecipe):
    # Assigns variables based on the given recipe
    # TODO: Actually pulls & assign things from the database
    name = "name"
    authorName = "authorName"
    description = "This is an example description. Look how long & wordy it is my gosh! Wowee, this person sure has a lot to say about this recipe don't you think? I hope you enjoyed reading that lol"
    tags = ["Example Tag 1", "Example Tag 2", "Example Tag 3"]
    defaultServings = 1000   # TODO: Allow the user to modify servings for their mealPlan
    ingredients = ["Example Ingredient 1", "Example Ingredient 2", "Example Ingredient 3", "Example Ingredient 4", "Example Ingredient 5"]
    steps = ["Example Step 1", "Example Step 2"]
    
    bar()
    # Name, author, description
    print(name + " -- By " + authorName)
    print("")
    print(description)
    print("")

    # Tags, default servings
    tagsListString = ""
    for i in tags:
        tagsListString += str(i) + ", "
    tagsListString = tagsListString[:-2]
    print("Tags: " + tagsListString)
    print("Default Servings: " + str(defaultServings))
    print("")

    # Ingredients & Allergens
    ingredientsListString = ""
    for i in ingredients:
        ingredientsListString += str(i) + ", "
    ingredientsListString = ingredientsListString[:-2]
    print("Ingredients: " + ingredientsListString)
    print("Allergens: ") # TODO: Extract allergens from ingredients
    print("")

    # Steps
    print("Steps:")
    for i in steps:
        print("   " + "#) " + str(i))
    
    bar()

#endregion ================================================================================================================

#region COMMANDS ==========================================================================================================

# ALL possible commands the user can enter
# IF YOU ADD ANYTHING HERE, ADD TO THE COMMANDMAP BELOW!!!!
# (Since these are userInputs, they should be written in all lowercase!)
class Command(Enum):
    login = auto() # TODO: Log In page asks for no command, just <yourusername yourpassword>
    createprofile = auto() # TODO: Create profile asks for <yourusername yourpassword>, then y/n
    createnewrecipe = auto()
    viewmyrecipes = auto()
    viewstarredrecipes = auto()
    viewmealplan = auto()
    searchrecipes = auto()
    logout = auto()
    editname = auto() # <name>
    addtag = auto() # <tagName>
    removetag = auto() # <tagName>
    editdescription = auto() # <description>
    addstep = auto() # <step text> # Add step (must be at least one)
    removestep = auto() # <step number>
    addingredient = auto() # <ingredient name> # Add ingredient (must be at least one)
    removeingredient = auto() # <ingredient name>
    returntoprofile = auto()
    editdefaultservings = auto() # <new quantity>
    deleterecipe = auto() # <recipe name>
    editrecipe = auto() # <recipe name>
    star = auto() # <recipe name>
    unstar = auto() # <recipe name>
    addtomealplan = auto() # <recipe name>
    removefrommealplan = auto() # <recipe name>
    editservings = auto() # <recipe name>
    search = auto() # <keywords>
    filter = auto() # <tag, allergen, or ingredient name> <name>
    submitRecipe = auto()

# Stores data specific to each command
# commandText -> the text that displays to the user
# behaviorFunction -> the function that executes the command
commandData = namedtuple('commandData', ['commandText', 'behaviorFunction'])

# Maps each command (the enumeration) to its data
# IF YOU ADD A COMMAND HERE, ADD IT TO PAGE(ENUM) AS WELL!!
# To access an instance of a command:
    # commandMap[commandInstance].commandText
    # commandMap[commandInstance].behaviorFunction()
commandMap = "" # We'll assign this variable at runtime
def createCommandMap():
    return {
        Command.login : commandData(commandText = "login <username> <password>", behaviorFunction = logIn()),
        Command.createprofile : commandData(commandText = "createprofile <username> <pasword>", behaviorFunction = createProfile()),
        Command.logout : commandData(commandText = "logout", behaviorFunction = logOut()),
        
        Command.createnewrecipe : commandData(commandText = "createnewrecipe", behaviorFunction = updatePage(Page.createNewRecipe)),
        Command.viewmyrecipes : commandData(commandText = "viewmyrecipes", behaviorFunction = updatePage(Page.myRecipes)),
        Command.viewstarredrecipes : commandData(commandText = "viewstarredrecipes", behaviorFunction = updatePage(Page.myStarredRecipes)),
        Command.viewmealplan : commandData(commandText = "viewmealplan", behaviorFunction = updatePage(Page.myMealPlan)),
        Command.searchrecipes : commandData(commandText = "searchrecipes", behaviorFunction = updatePage(Page.searchRecipes)),
        Command.returntoprofile : commandData(commandText = "returntoprofile", behaviorFunction = updatePage(Page.userProfile)),
        Command.editrecipe : commandData(commandText = "editrecipe <recipeID>", behaviorFunction = updatePage(Page.editRecipe)), # <recipe name>  # TODO: command function, not a page

        Command.editname : commandData(commandText = "editname <newname>", behaviorFunction = editRecipeName()), # <name>
        Command.addtag : commandData(commandText = "addtag <tagname>", behaviorFunction = addRecipeTag()), # <tagName>
        Command.removetag : commandData(commandText = "removetag <tagname>", behaviorFunction = removeRecipeTag()), # <tagName>
        Command.editdescription : commandData(commandText = "editdescription <newdescription>", behaviorFunction = editRecipeDescription()), # <description>
        Command.addstep : commandData(commandText = "addstep <newstep>", behaviorFunction = addRecipeStep()), # <step text> # Add step (must be at least one)
        Command.removestep : commandData(commandText = "removestep <stepnumber>", behaviorFunction = removeRecipeStep()), # <step number>
        Command.addingredient : commandData(commandText = "addingredient <ingredientID>", behaviorFunction = addRecipeIngredient()), # <ingredient name> # Add ingredient (must be at least one)
        Command.removeingredient : commandData(commandText = "removeingredient <ingredientID>", behaviorFunction = removeRecipeIngredient()), # <ingredient name>
        Command.editdefaultservings : commandData(commandText = "editdefaultservings <quantity>", behaviorFunction = editRecipeDefaultServings()), # <new quantity>
        Command.submitRecipe : commandData(commandText = "submitRecipe", behaviorFunction = submitRecipe()),

        Command.deleterecipe : commandData(commandText = "deleterecipe <recipeID>", behaviorFunction = deleteRecipe()), # <recipe name>
        Command.star : commandData(commandText = "star <recipeID>", behaviorFunction = starRecipe()), # <recipe name>
        Command.unstar : commandData(commandText = "unstar <recipeID>", behaviorFunction = unstarRecipe()), # <recipe name>
        Command.addtomealplan : commandData(commandText = "addtomealplan <recipeID>", behaviorFunction = addMealPlanRecipe()), # <recipe name>
        Command.removefrommealplan : commandData(commandText = "removefrommealplan <recipeID>", behaviorFunction = removeMealPlanRecipe()), # <recipe name>
        Command.editservings : commandData(commandText = "editservings <recipeID> <newquantity>", behaviorFunction = editServings()), # <recipe name>
        
        Command.search : commandData(commandText = "search <searchterm>", behaviorFunction = searchRecipes()), # <keywords>
        Command.filter : commandData(commandText = "filter <tag/allergen/ingredient> <name>", behaviorFunction = filterBy()), # <tag, allergen, or ingredient name> <name>
    }

#endregion ================================================================================================================

#region USER INPUT FUNCTIONS ==============================================================================================

# The line the user types in
userInput = ""
# userInput parsed into a list by its individual words
userInputList = []
# index 0 of userInputList, the actual command word(s) the user enters, should always be lower()
userCommand = ""

# Prints out the list of available commands & gathers the user's input
# commandList -> a list of strings of the commands available to the user from this page
def getUserInput(commandList):
    global userInput
    global userInputList
    global userCommand

    # Prints the commands available to the user
    print("")
    print("Enter one of the following commands: ")
    for i in commandList:
        print(i.commandText)
    
    # Takes user input
    userInput = input(">>> ").strip()
    userInputList = userInput.split()
    userCommand = userInputList[0].lower() if userInputList else "" # the if-else sets the command to an empty string if there is no command

#endregion ================================================================================================================

#region DISPLAY PAGES =======================================================================================================

def runCurrentPage():
    # Sets up global variables
    global pageMap
    global currentPage
    global previousPage
    global userInput
    global userInputList
    global userCommand

    # Displays the title
    displayTitle(currentPage)

    # Calls page-specific behavior (displays, commands etc.)
    pageMap[currentPage].behaviorFunction()

#endregion ==================================================================================================================

#region PAGE BEHAVIOR FUNCTIONS =============================================================================================
    
def homePage():
    print("Brought to you by Lina Boughton, Luna Gal, & Diya Misra")
    # Turns user input into navigation
    pageCommands = [Command.login, Command.createprofile]
    getUserInput(pageCommands)

    for i in pageCommands:
        if userCommand == i:
            commandMap[i].behaviorFunction()
            return
    # If command not recognized
    print("Command not recognized, please try again.")

def userProfile():
    # Turns user input into navigation
    pageCommands = [Command.createnewrecipe, Command.viewmyrecipes, Command.viewstarredrecipes, Command.viewmealplan, Command.searchrecipes, Command.logout]
    getUserInput(pageCommands)

    for i in pageCommands:
        if userCommand == i:
            commandMap[i].behaviorFunction()
            return
    # If command not recognized
    print("Command not recognized, please try again.")

def createNewRecipe():
    displayRecipe(newRecipe) # TODO: actually create a new recipe here

    # Turns user input into navigation
    pageCommands = [Command.editname, Command.editdescription, Command.addtag, Command.removetag, Command.editservings, Command.addingredient, Command.removeingredient, Command.addstep, Command.removestep, Command.submitRecipe, Command.returntoprofile]
    getUserInput(pageCommands)

    for i in pageCommands:
        if userCommand == i:
            commandMap[i].behaviorFunction()
            return
    # If command not recognized
    print("Command not recognized, please try again.")

def myRecipes():
    # TODO: For i in myRecipes
    # displayRecipe(i)

    # Turns user input into navigation
    pageCommands = [Command.deleterecipe, Command.editrecipe, Command.star, Command.unstar, Command.addtomealplan, Command.removefrommealplan, Command.returntoprofile]
    getUserInput(pageCommands)

    for i in pageCommands:
        if userCommand == i:
            commandMap[i].behaviorFunction()
            return
    # If command not recognized
    print("Command not recognized, please try again.")

def myStarredRecipes():
    # TODO: For i in myStarredRecipes
    # displayRecipe(i)

    # Turns user input into navigation
    pageCommands = [Command.unstar, Command.addtomealplan, Command.removefrommealplan, Command.returntoprofile]
    getUserInput(pageCommands)

    for i in pageCommands:
        if userCommand == i:
            commandMap[i].behaviorFunction()
            return
    # If command not recognized
    print("Command not recognized, please try again.")

def myMealPlan():
    # TODO: For i in myMealPlan
    # displayRecipe(i)

    # Turns user input into navigation
    pageCommands = [Command.removefrommealplan, Command.star, Command.unstar, Command.editservings, Command.returntoprofile]
    getUserInput(pageCommands)

    for i in pageCommands:
        if userCommand == i:
            commandMap[i].behaviorFunction()
            return
    # If command not recognized
    print("Command not recognized, please try again.")

def searchRecipes():
    # TODO: For i in Recipes (All recipes!!)
    # displayRecipe(i)

    # Turns user input into navigation
    pageCommands = [Command.search, Command.filter, Command.star, Command.unstar, Command.addtomealplan, Command.removefrommealplan, Command.returntoprofile]
    getUserInput(pageCommands)

    for i in pageCommands:
        if userCommand == i:
            commandMap[i].behaviorFunction()
            return
    # If command not recognized
    print("Command not recognized, please try again.")

def editRecipe(): # TODO: editRecipe should be a command??? Not a page...
    print("TestMessage: Recipe edited!")
    
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

#endregion ==================================================================================================================

#region COMMAND BEHAVIOR FUNCTIONS ==========================================================================================

# Ensures the command was given with the right amount of inputs
def checkUserInputListLength(requiredInputs):
    global userInputList

    if len(userInputList) < (requiredInputs + 1):
        print("Error: Not enough inputs given")
        return True
    return False

# LOGIN/CREATEPROFILE/LOGOUT

def logIn(): # <username> <password>
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(2): return
    enteredUsername = userInputList[1]
    enteredPassword = userInputList[1]
    
    # TODO: Checks for proper username-password combo in the database
    print("TestMessage: Logged in: " + enteredUsername + " " + enteredPassword)
    # TODO: loggedInUser = user in database!
    # TODO: Populates userProfile with userInfo
    updatePage(Page.userProfile)

def createProfile(): # <username> <password>
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(2): return
    enteredUsername = userInputList[1]
    enteredPassword = userInputList[1]
    
    # TODO: create the user in the database
    print("TestMessage: profile created: " + enteredUsername + " " + enteredPassword)
    # TODO: Populates userProfile with userInfo
    updatePage(Page.userProfile)
    print("TestMessge: Profile created!")

def logOut():
    print("TestMessage: Logged Out!")
    loggedInUser = ""
    updatePage(Page.home)

# ALL OF THESE OCCUR WITHIN CREATE/EDIT RECIPE

def editRecipeName(): # <new name>
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(1): return
    newName = userInputList[1]
    
    print("TestMessage: updated name to " + newName)
    # TODO: Update the name in the database

def addRecipeTag(): # <tagName>
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(1): return
    tagName = userInputList[1]
    
    print("TestMessage: added tag " + tagName)
    # TODO: in database

def removeRecipeTag(): # <tagName>
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(1): return
    tagName = userInputList[1]
    
    print("TestMessage: removed tag " + tagName)
    # TODO: in database

def editRecipeDescription(): # <description>
    #TODO: with the way this is coded, description can only be 1 word! Mayhaps make a new function that will ask the user for more input & take everything they say.
    # ^^ TODO: Use this function for searchRecipes, addstep, etc. too!
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(1): return
    newDescription = userInputList[1]
    
    print("TestMessage: new description: " + newDescription)
    # TODO: in database

def addRecipeStep(): # <step text>
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(1): return
    newStep = userInputList[1]
    
    print("TestMessage: new step: " + newStep)
    # TODO: in database

def removeRecipeStep(): # <step number>
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(1): return
    stepNumber = userInputList[1]
    
    print("TestMessage: removed step: " + stepNumber)
    # TODO: in database

def addRecipeIngredient(): # <ingredientID> (must be at least one ingredient in the recipe)
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(1): return
    newIngredient = userInputList[1]
    
    print("TestMessage: new ingredient: " + newIngredient)
    # TODO: in database

def removeRecipeIngredient(): # <ingredientID>
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(1): return
    ingredientToRemove = userInputList[1]
    
    print("TestMessage: removed ingredient: " + ingredientToRemove)
    # TODO: in database

def editRecipeDefaultServings(): # <new servings quantitiy>
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(1): return
    newQuantity = userInputList[1]
    
    print("TestMessage: updated default quantity: " + newQuantity)
    # TODO: in database

def submitRecipe():
    global userInputList
    # TODO: Check that the recipe has a name, at least 1 step, at least 1 ingredient
    print("Recipe created!")
    # TODO: in database
    updatePage(Page.myRecipes)

# MYRECIPES/MEALPLAN/STARREDRECIPES

#TODO: Display recipes needs to display recipeID as well! Ingredients should also display their ID!

def deleteRecipe(): # <recipeID>
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(1): return
    recipeToDelete = userInputList[1]
    print("TestMessage: deleted " + recipeToDelete)
    # TODO: deleterecipe in database

def starRecipe(): # <recipeID>
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(1): return
    recipeToStar = userInputList[1]
    print("TestMessage: starred " + recipeToStar)
    # TODO: star in database

def unstarRecipe(): # <recipeID>
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(1): return
    recipeToUnstar = userInputList[1]
    print("TestMessage: unstarred " + recipeToUnstar)
    #TODO: Actually unnstar this recipe in the database

def addMealPlanRecipe(): # <recipeID>
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(1): return
    recipeToAdd = userInputList[1]
    print("TestMessage: added to meal plan:  " + recipeToAdd)
    #TODO: Actually add this recipe to meal plan in the database

def removeMealPlanRecipe(): # <recipeID>
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(1): return
    recipeToRemove = userInputList[1]
    print("TestMessage: removed from meal plan:  " + recipeToRemove)
    #TODO: Actually remove this recipe from meal plan in the database

def editServings(): # <recipeID> <new quantity> (Note: refers to meal plan servings)
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(2): return
    
    recipeToEdit = userInputList[1]
    newQuantity = userInputList[2]
    print("TestMessage: edited servings for recipe " + recipeToEdit + " to " + newQuantity)
    #TODO: Actually edit servings in database

# SEARCH RECIPES

def searchRecipes(): # <keyword>
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(1): return
    
    keyword = userInputList[1]
    print("TestMessage: searched with keyword " + keyword)
    #TODO: Actually search in database & output stuff here!

def filterBy(): # <tag, allergen, or ingredient type> <name>
    global userInputList
    # If there are not enough inputs with the command, exit prematurely
    if checkUserInputListLength(2): return
    
    filterType = userInputList[1]
    name = userInputList[2]
    print("TestMessage: filtered with type " + filterType + " for " + name)
    #TODO: Actually filter & output stuff

#endregion ==================================================================================================================

#region EXECUTING THE CODE =================================================================================================

# Please use the with ... as block (-Luna)
# It ensures that connection commits everything to the database when the program finishes
def run_app(host=host, user=user, password=password):
    with RecipeDBConnection(host, user, password, dbname) as connection:
        # Sets the initial page to the homePage
        global currentPage
        currentPage = Page.home

        # Creates the pageMap & commandMap
        global pageMap
        pageMap = createPageMap()
        global commandMap
        commandMap = createCommandMap()

        # Forever calls the currentPage to execute its behaviors
        while True:
            runCurrentPage(pageMap[currentPage])

run_app()

#endregion ==================================================================================================================