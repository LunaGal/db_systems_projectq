import mysql.connector

class RecipeDBConnection:
    RecipesCols = ["Recipe_Name", "Recipe_Description", "Author_Name", "Default_Servings"]

    def __init__(self, host, user, password, dbname):
        self.db = mysql.connector.connect(host=host,
                                          user=user,
                                          password=password)
        self.dbcursor = self.db.cursor()
        self.dbcursor.execute(f"use {dbname}")

    # Create

    # Add user to database
    def makeUser(self, username, password):
        try:
            self.dbcursor.execute(f"insert into users values (\"{username}\", \"{password})\"")
            return True
        except mysql.connector.InterfaceError:
            return False

    # Takes a recipe as a dictionary and inserts it into database
    # Current implementation doesn't support steps
    # If you pass in a recipe with unexpected fields, the fields are ignored
    def makeRecipe(self, recipe):

        cols = [x for x in RecipeDBConnection.RecipesCols if x in recipe]
        vals = ["'" + recipe[x] + "'" for x in cols]

        cols_str = ",".join(cols)
        vals_str = ",".join(vals)

        statement = f"insert into recipes (RecipeID, {cols_str}) values (UUID_TO_BIN(UUID()), {vals_str});"

        self.dbcursor.execute(statement)

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

    # Other

    def close(self):
        self.db.commit()
        self.db.close()

    def __del__(self):
        self.close

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close() 

