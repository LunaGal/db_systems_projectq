import mysql.connector

class RecipeDBConnection:
    def __init__(self, host, user, password):
        self.db = mysql.connector.connect(host=host,
                                          user=user,
                                          password=password)
        self.dbcursor = self.db.cursor()

    # Create

    def makeUser(self, username, password):
        try:
            self.dbcursor.execute(f"insert into users values (\"{username}\", \"{password})\"")
            return True
        except mysql.connector.InterfaceError:
            return False

    def makeRecipe(self, recipe):
        
        return None


    # Update

    ## Starred

    def setStarred(username, recipe, starred):
        return None


    ## Meal Plan

    def addPlannedMeal(username, recipe, servings):
        return None

    def removePlannedMeal(username, recipe):
        return None

    def changeServings(username, recipe, newServings):
        return None

    ## Recipe

    def changeRecipe(newvalues):
        return None

    def addRecipeStep(step, position=0):
        return None

    # Retrieve
    # These functions will return dictionaries representing the entry in the database

    ## User

    # returns true if password matches password of user, false otherwise
    def isPassword(user, password):
        return None

    ## Meal Plan

    def getMealPlan(user):
        return None

    ## Recipe

    def getRecipeID(recipeID):
        return None

    def searchRecipe(attributes):
        return None

    # Delete

    def deleteUser(username):
        return None

    def deleteRecipe(recipeID):
        return None

