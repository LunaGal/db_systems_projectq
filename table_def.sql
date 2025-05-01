create table Users (
	Username varchar(40) not NULL,
    User_Password varchar(40) not NULL,
    Constraint pk_username Primary Key (Username)
);

Create table Recipes (
	RecipeID binary(16) not null,
    Recipe_Name varchar(40) not null,
    Recipe_Description varchar(1500),
    Author_Name varchar(40) not null,
    Default_Servings int not null,
    Constraint pk_recipeid Primary Key(RecipeID),
    Constraint fk_authorname Foreign Key(Author_Name) References Users(Username)
);

Create table Meal_Plans (
	MealPlanID binary(16) not null,
    Username varchar(40) not null,
    RecipeID binary(16) not null,
    Servings int,
    Constraint pk_mealplanid Primary Key (MealPlanID),
    Constraint fk_username Foreign Key (Username) References Users(Username),
    Constraint fk_recipeid Foreign Key (RecipeID) References Recipes(RecipeID)
);

create table User_Starred_Recipes (
	Username varchar(40) not null,
	RecipeID binary(16) not null,
	Constraint pk_Username_RecipeID Primary Key (Username, RecipeID),
	Constraint fk_Username_Starred Foreign Key (Username) references Users(Username)
);

create table Recipe_Steps (
	RecipeID binary(16) not null,
    Step varchar(40),
    Step_Number int not null,
    Constraint pk_Recipe_Steps Primary Key (RecipeID, Step_Number),
    Constraint fk_recipeid_steps Foreign Key (RecipeID) References Recipes(RecipeID)
);

create table Tags (
	RecipeID binary(16) not null,
    Tag_name varchar(40) not null,
    Constraint pk_Tags Primary Key (RecipeID, Tag_name),
    Constraint fk_recipeid_tags Foreign Key (RecipeID) References Recipes(RecipeID)
);

create table Ingredients (
	IngredientID binary(16) not null,
    Ingredient_Name varchar(70) not null,
    Constraint pk_ingredientID Primary Key (IngredientID)
);

create table Recipe_Ingredients (
	RecipeID binary(16) not null,
    IngredientID binary(16) not null,
    Quantity float not null,
    Constraint pk_recipeId Primary Key (RecipeID, IngredientID),
    Constraint fk_recipeID_recips Foreign Key (RecipeID) references Recipes(RecipeID),
    Constraint fk_ingredientID_recips Foreign Key (IngredientID) references Ingredients(IngredientID)
);

create table Allergens (
	AllergenID binary(16) not null,
    Allergen_Name varchar(70) not null,
    IngredientID binary(16) not null,
    Constraint pk_allergenID_ingredientID Primary Key (AllergenID, IngredientID),
    Constraint fk_ingredientID Foreign Key (IngredientID) references Ingredients(IngredientID)
);

create table Substitutions (
	Substitution varchar(70) not null,
    IngredientID binary(16) not null,
    Constraint pk_substitution_ingredientID Primary Key (Substitution, IngredientID),
    Constraint fk_ingredientID_subs Foreign Key (IngredientID) references Ingredients(IngredientID)
);

