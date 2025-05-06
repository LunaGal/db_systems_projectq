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
        self.dbcursor = self.db.cursor(buffered=True)
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
    # If you pass in a recipe with unexpected fields, the fields are ignored
    # Returns true if succesfully inserted, false if integrity error
    # Typical cause of integrity error is putting in a recipe + username combo that already exists
    def makeRecipe(self, recipe):

        cols = [x for x in RecipeDBConnection.RecipesCols if x in recipe]
        vals = ["'" + str(recipe[x]) + "'" for x in cols]

        cols_str = ",".join(cols)
        vals_str = ",".join(vals)

        self.dbcursor.execute("select uuid_to_bin(uuid())")

        id = self.dbcursor.fetchone()[0]

        statement = f"insert into recipes (RecipeID, {cols_str}) values (%s, {vals_str});"

        try:
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
        
        except mysql.connector.IntegrityError:
            return False

        return True

    def addIngredient(self, name):
        statement = "insert into Ingredients Values (uuid_to_bin(uuid()), %s)"
        self.dbcursor.execute(statement, (name, ))

    
    
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
        self.dbcursor.execute("select uuid_to_bin(uuid())")
        id = self.dbcursor.fetchone()[0]

        try:
            statement = "insert into Meal_Plans values (%s, %s, %s, %s);"
            self.dbcursor.execute(statement, (id, username, recipe, servings))
        except mysql.connector.IntegrityError:
            return False
        
        return True

    def removePlannedMeal(self, mealPlanID):
        statement = "delete from Meal_Plans where MealPlanID = %s"
        self.dbcursor.execute(statement, (mealPlanID, ))

    def changeServings(self, mealPlanID, newServings):
        statement = "update Meal_Plans set servings = %s where mealPlanID = %s"
        self.dbcursor.execute(statement, (newServings, mealPlanID))

    ## Recipe

    # newValues should be a dictionary with field : newValue
    # Still needs ability to set steps, ingredients, tags
    def changeRecipe(self, recipeID, newValues):
        cols = [x for x in RecipeDBConnection.RecipesCols if x in newValues]
        vals = ["'" + str(newValues[x]) + "'" for x in cols]
        sets = ",".join([f" {col} = {val}" for col, val in zip(cols, vals)])

        statement = f"update recipes set {sets} where RecipeID = %s;"

        self.dbcursor.execute(statement, (recipeID, ))
        return None

    def addRecipeStep(self, recipeID, step, position=-1):
        if (position >= 0):
            statement = f"update Recipe_Steps set step_number = step_number + 1 where recipeid = %s and step_number >= %s order by step_number desc;"
            self.dbcursor.execute(statement, (recipeID, position))
        else:
            statement = f"select step_number from recipe_steps where recipe_id = %s order by step_number"
            self.dbcursor.execute(statement, (recipeID, ))
            position = [x for x in self.dbcursor][0][0]
        statement = f"insert into Recipe_Steps Values (%s, %s, %s)"
        self.dbcursor.execute(statement, (recipeID, step, position))
        return None

    # Retrieve
    # These functions will return dictionaries representing the entry in the database

    ## User

    # returns true if password matches password of user, false otherwise
    def isPassword(self, user, password):
        statement = f"select * from Users where username = %s and user_password = %s"
        self.dbcursor.execute(statement, (user, password))

        return (len([x for x in self.dbcursor]) > 0)

    ## Meal Plan

    def getMealPlan(self, user):
        statement = f"select * from Meal_Plans where Username = %s"
        self.dbcursor.execute(statement, (user, ))
        return [dict(zip(["MealPlanID", "Username", "RecipeID", "Servings"], x)) for x in self.dbcursor]

    ## Recipe

    # Fetches recipe as a tuple
    # Later version will format it nicely as a dictionary
    def getRecipeByID(self, recipeID):
        statement = "select * from Recipes where RecipeID = %s";
        self.dbcursor.execute(statement, (recipeID, ))
        entry = [x for x in self.dbcursor][0]
        recipe = dict(zip(["RecipeID"] + RecipeDBConnection.RecipesCols, entry))
        
        statement = "select step from Recipe_Steps where RecipeID = %s order by step_number"
        self.dbcursor.execute(statement, (recipeID, ))
        recipe["Recipe_Steps"] = [x[0] for x in self.dbcursor]
        
        statement = "select IngredientID, Quantity from Recipe_Ingredients where RecipeID = %s"
        self.dbcursor.execute(statement, (recipeID, ))
        recipe["Recipe_Ingredients"] = [x for x in self.dbcursor]
        
        statement = "select Tag_name from Tags where RecipeID = %s"
        self.dbcursor.execute(statement, (recipeID, ))
        recipe["Tags"] = [x[0] for x in self.dbcursor]

        return recipe

    # A bit inefficient but idc at this point
    def searchRecipe(self, recipe):
        where = " and ".join([f"{field} = '{recipe[field]}'" for field in recipe])

        statement = f"select recipeid from Recipes where {where}"
        self.dbcursor.execute(statement)

        recipes = []
        queries = [x for x in self.dbcursor]

        for x in queries:
            recipe = self.getRecipeByID(x[0])
            recipes.append(recipe)

        return recipes
    
    def searchRecipeByAllergen(self, allergenName):
        statement = "select Recipe_Ingredients.RecipeID from Recipe_Ingredients inner join Allergens on Recipe_Ingredients.IngredientID = Allergens.IngredientID where Allergen_Name = %s;"
        self.dbcursor.execute(statement, (allergenName))

        recipes = []
        queries = [x for x in self.dbcursor]

        for x in queries:
            recipe = self.getRecipeByID(x[0])
            recipes.append(recipe)

        return recipes
    
    def searchRecipeByTag(self, tagName):
        statement = "select Recipes.RecipeID from Recipes inner join Tags on Recipes.RecipeID=Tags.RecipeID where Tags.tag_name = /s;"
        self.dbcursor.execute(statement, (tagName))

        recipes = []
        queries = [x for x in self.dbcursor]

        for x in queries:
            recipe = self.getRecipeByID(x[0])
            recipes.append(recipe)

        return recipes
    
    def searchRecipeByIngredient(self, ingredientName):
        statement = "select Recipes.RecipeID from Recipes inner join Recipe_Ingredients on Recipes.RecipeID=Recipe_Ingredients.RecipeID inner join Ingredients on Recipe_Ingredients.IngredientID=Ingredients.IngredientID where Ingredients.Ingredient_Name = %s"
        self.dbcursor.execute(statement, (ingredientName))

        recipes = []
        queries = [x for x in self.dbcursor]

        for x in queries:
            recipe = self.getRecipeByID(x[0])
            recipes.append(recipe)

        return recipes

    ## Ingredients

    # Returns as tuples because Ingredients aren't really complex enough to represent as dicts
    # shape is (ingredientid, ingredient_name)
    def getAllIngredients(self):
        statement = "select * from Ingredients;"
        self.dbcursor.execute(statement)
        return [x for x in self.dbcursor]
    
    # Returns a list of ingredients with a specified name
    def getIngredientsByName(self, name):
        statement = "select * from Ingredients where Ingredient_Name = %s"
        self.dbcursor.execute(statement, (name, ))
        return [x for x in self.dbcursor]


    # Delete

    def deleteUser(self, username):
        statement = f"delete from Users where username = %s"
        self.dbcursor.execute(statement, (username, ))
        return None

    def deleteRecipe(self, recipeID):
        statement = f"delete from Recipes where RecipeID = %s"
        self.dbcursor.execute(statement, (recipeID, ))
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

