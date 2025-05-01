INSERT INTO Users (Username, User_Password) VALUES 
('goodboi123', 'iluvbones'),
('barktastic', 'woofwoofwoof'),
('chewchewtrain', 'password123'),
('pupperchef', 'hotsnackz'),
('floofygal', 'dogsrule');


INSERT INTO Recipes (RecipeID, Recipe_Name, Recipe_Description, Author_Name, Default_Servings) VALUES 
(uuid_to_bin(uuid()), 'Bark-B-Q Ribs', 'Slow cooked squirrel ribs slathered in bone marrow sauce', 'goodboi123', 2),
(uuid_to_bin(uuid()), 'Peanut Butter Pupperoni', 'A rich snack made with organic peanut butter and artificial bacon', 'barktastic', 4),
(uuid_to_bin(uuid()), 'Squirrel Surprise', 'You think it’s tofu, but it’s squirrel. A classic prank dish.', 'pupperchef', 3),
(uuid_to_bin(uuid()), 'Trashcan Tapenade', 'A bold, urban take using ingredients sourced from alleyways', 'chewchewtrain', 1),
(uuid_to_bin(uuid()), 'Chicken ''n'' Tennis Balls', 'A mix of chewable and edible. Not recommended for humans.', 'floofygal', 5);

;

INSERT INTO Meal_Plans (MealPlanID, Username, RecipeID, Servings) VALUES 
(uuid_to_bin(uuid()), 'goodboi123', (select recipeid from recipes where recipe_name='Peanut Butter Pupperoni'), 4),
(uuid_to_bin(uuid()), 'chewchewtrain', (select recipeid from recipes where recipe_name='Bark-B-Q Ribs'), 1),
(uuid_to_bin(uuid()), 'floofygal', (select recipeid from recipes where recipe_name='Chicken ''n'' Tennis Balls'), 3),
(uuid_to_bin(uuid()), 'barktastic', (select recipeid from recipes where recipe_name='Trashcan Tapenade'), 2),
(uuid_to_bin(uuid()), 'pupperchef', (select recipeid from recipes where recipe_name='Squirrel Surprise'), 3);

INSERT INTO User_Starred_Recipes (Username, RecipeID) VALUES 
('goodboi123', (select recipeid from recipes where recipe_name='Chicken ''n'' Tennis Balls')),
('chewchewtrain', (select recipeid from recipes where recipe_name='Peanut Butter Pupperoni')),
('barktastic', (select recipeid from recipes where recipe_name='Bark-B-Q Ribs')),
('floofygal', (select recipeid from recipes where recipe_name='Squirrel Surprise')),
('pupperchef', (select recipeid from recipes where recipe_name='Trashcan Tapenade'));

INSERT INTO Recipe_Steps (RecipeID, Step, Step_Number) VALUES 
((select recipeid from recipes where recipe_name='Bark-B-Q Ribs'), 'Dig hole and marinate ribs underground', 1),
((select recipeid from recipes where recipe_name='Bark-B-Q Ribs'), 'Howl at the moon while it cooks', 2),
((select recipeid from recipes where recipe_name='Peanut Butter Pupperoni'), 'Open jar of peanut butter with snout', 1),
((select recipeid from recipes where recipe_name='Peanut Butter Pupperoni'), 'Stir in pupperoni bits', 2),
((select recipeid from recipes where recipe_name='Squirrel Surprise'), 'Catch squirrel', 1),
((select recipeid from recipes where recipe_name='Squirrel Surprise'), 'Pretend it''s tofu', 2),
((select recipeid from recipes where recipe_name='Trashcan Tapenade'), 'Find best trashcan', 1),
((select recipeid from recipes where recipe_name='Trashcan Tapenade'), 'Extract semi-edible contents', 2),
((select recipeid from recipes where recipe_name='Chicken ''n'' Tennis Balls'), 'Boil chicken and serve on tennis balls', 1),
((select recipeid from recipes where recipe_name='Chicken ''n'' Tennis Balls'), 'Retrieve and repeat', 2);

INSERT INTO Tags (RecipeID, Tag_name) VALUES 
((select recipeid from recipes where recipe_name='Bark-B-Q Ribs'), 'BBQ'),
((select recipeid from recipes where recipe_name='Peanut Butter Pupperoni'), 'Snack'),
((select recipeid from recipes where recipe_name='Squirrel Surprise'), 'Prank'),
((select recipeid from recipes where recipe_name='Trashcan Tapenade'), 'Foraged'),
((select recipeid from recipes where recipe_name='Chicken ''n'' Tennis Balls'), 'Chewy'),
((select recipeid from recipes where recipe_name='Chicken ''n'' Tennis Balls'), 'Birthday');

INSERT INTO Ingredients (IngredientID, Ingredient_Name) VALUES 
(uuid_to_bin(uuid()), 'Squirrel'),
(uuid_to_bin(uuid()), 'Peanut Butter'),
(uuid_to_bin(uuid()), 'Pupperoni'),
(uuid_to_bin(uuid()), 'Chicken'),
(uuid_to_bin(uuid()), 'Tennis Ball'),
(uuid_to_bin(uuid()), 'Bone Marrow Sauce'),
(uuid_to_bin(uuid()), 'Trash Bits'),
(uuid_to_bin(uuid()), 'Tofu');

INSERT INTO Recipe_Ingredients (RecipeID, IngredientID, Quantity) VALUES 
((select recipeid from recipes where recipe_name='Bark-B-Q Ribs'), (select ingredientid from ingredients where ingredient_name='Squirrel'), 2),
((select recipeid from recipes where recipe_name='Bark-B-Q Ribs'), (select ingredientid from ingredients where ingredient_name='Bone Marrow Sauce'), 0.5),
((select recipeid from recipes where recipe_name='Peanut Butter Pupperoni'), (select ingredientid from ingredients where ingredient_name='Peanut Butter'), 1.0),
((select recipeid from recipes where recipe_name='Peanut Butter Pupperoni'), (select ingredientid from ingredients where ingredient_name='Pupperoni'), 0.25),
((select recipeid from recipes where recipe_name='Squirrel Surprise'), (select ingredientid from ingredients where ingredient_name='Squirrel'), 1),
((select recipeid from recipes where recipe_name='Squirrel Surprise'), (select ingredientid from ingredients where ingredient_name='Tofu'), 0.1),
((select recipeid from recipes where recipe_name='Trashcan Tapenade'), (select ingredientid from ingredients where ingredient_name='Trash Bits'), 2.0),
((select recipeid from recipes where recipe_name='Chicken ''n'' Tennis Balls'), (select ingredientid from ingredients where ingredient_name='Chicken'), 3),
((select recipeid from recipes where recipe_name='Chicken ''n'' Tennis Balls'), (select ingredientid from ingredients where ingredient_name='Tennis Ball'), 5);

INSERT INTO Allergens (AllergenID, Allergen_Name, IngredientID) VALUES 
(1, 'Peanuts', (select ingredientid from ingredients where ingredient_name='Peanut Butter')),
(2, 'Soy', (select ingredientid from ingredients where ingredient_name='Tofu')),
(3, 'Latex', (select ingredientid from ingredients where ingredient_name='Tennis Ball'));

INSERT INTO Substitutions (Substitution, IngredientID) VALUES 
('Pumpkin Puree', (select ingredientid from ingredients where ingredient_name='Peanut Butter')),
('Carrot Bits', (select ingredientid from ingredients where ingredient_name='Pupperoni')),
('Catnip-Infused Tofu', (select ingredientid from ingredients where ingredient_name='Tofu')),
('Old Sock', (select ingredientid from ingredients where ingredient_name='Trash Bits')),
('Rubber Ball', (select ingredientid from ingredients where ingredient_name='Tennis Ball'));

