import mysql.connector

def entryToDict(fields, colNames):
    assert(len(fields) == len(colNames))
    return dict(zip(colNames, fields))

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
    # Return True if successful, false otherwise
    def makeUser(self, username, password):
        try:
            self.dbcursor.execute(f"insert into users values (\"{username}\", \"{password}\");")
            return True
        except mysql.connector.IntegrityError:
            return False

    # Takes a recipe as a dictionary and inserts it into database
    # Current implementation doesn't support steps
    # If you pass in a recipe with unexpected fields, the fields are ignored
    def makeRecipe(self, recipe):

        cols = [x for x in RecipeDBConnection.RecipesCols if x in recipe]
        vals = ["'" + str(recipe[x]) + "'" for x in cols]

        cols_str = ",".join(cols)
        vals_str = ",".join(vals)

        self.dbcursor.execute("select uuid_to_bin(uuid())")

        id = self.dbcursor.fetchone()[0]

        statement = f"insert into recipes (RecipeID, {cols_str}) values (%s, {vals_str});"

        self.dbcursor.execute(statement, (id, ))

        if "Recipe_Steps" in recipe:
            for step_number, step in enumerate(recipe["Recipe_Steps"]):
                statement = "insert into Recipe_Steps Values (%s, %s, %s)"
                self.dbcursor.execute(statement, (id, step, step_number))

        if "Recipe_Ingredients" in recipe:
            for ingredientID, quantity in recipe["Recipe_Ingredients"]:
                statement = "insert into Recipe_Ingredients Values (%s, %s, %s)"
                self.dbcursor.execute(statement, (id, ingredientID, quantity))

        if "Tags" in recipe:
            for tagName in recipe["Tags"]:
                statement = "insert into Tags Values (%s, %s)"
                self.dbcursor.execute(statement, (id, tagName))

        return None


    # Update

    ## Starred

    # If starred, stars recipeID for username
    # Otherwise unstars it
    def setStarred(self, username, recipeID, starred):
        if starred:
            statement = "insert ignore into User_Starred_Recipes set username = %s, RecipeID = %s;"
            self.dbcursor.execute(statement, (username, recipeID))
        else:
            statement = "delete from User_Starred_Recipes where username = %s and RecipeID = %s;"
            self.dbcursor.execute(statement, (username, recipeID))


    ## Meal Plan

    def addPlannedMeal(self, username, recipe, servings):
        statement = "insert into Meal_Plans (uuid_to_bin(uuid()), %s, %s, %s);"
        self.dbcursor.execute(statement, (username, recipe, servings))

    def removePlannedMeal(self, mealPlanID):
        statement = "delete from Meal_Plans where MealPlanID = %s"
        self.dbcursor.execute(statement, (mealPlanID, ))

    def changeServings(self, mealPlanID, newServings):
        statement = "update Meal_Plans set servings = %s where mealPlanID = %s"
        self.dbcursor(statement, (newServings, mealPlanID))

    ## Recipe

    # newValues should be a dictionary with field : newValue
    # Still needs ability to set steps, ingredients, tags
    def changeRecipe(self, recipeID, newValues):
        cols = [x for x in RecipeDBConnection.RecipesCols if x in newValues]
        vals = ["'" + str(newValues[x]) + "'" for x in cols]
        sets = ",".join([f"set {col} = {val}" for col, val in zip(cols, vals)])

        statement = f"update recipes set {sets} where RecipeID = %s;"

        self.dbcursor.execute(statement, (recipeID, ))
        return None

    def addRecipeStep(step, position=-1):
        return None

    # Retrieve
    # These functions will return dictionaries representing the entry in the database

    ## User

    # returns true if password matches password of user, false otherwise
    def isPassword(self, user, password):
        statement = f""
        return None

    ## Meal Plan

    def getMealPlan(self, user):
        statement = f"select * from Meal_Plans where Username = %s"
        self.dbcursor.execute(statement, (user, ))
        return None

    ## Recipe

    # Fetches recipe as a tuple
    # Later version will format it nicely as a dictionary
    def getRecipeByID(self, recipeID):
        statement = f"select * from Recipes where RecipeID = %s";
        self.mycursor.execute(statement, recipeID)
        return self.mycursor.fetchone()

    def searchRecipe(recipe):
        statement = f"select * from Recipes where "
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

