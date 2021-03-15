Files for creating the webapp located at goosej-recipes.herokuapp.com

Files not uploaded to github due to size limitations:
	Cached folder of htmls
	json files
	trained models

FILES:

scraper.py

This file goes throughn the supported recipe websites, builds a list of urls to extract recipe data from. Then caches html files for data extraction.

extract.py

This file will go through all the cached htmls and uncached htmls that are in the url list and extract relevant recipe data.  These are then saved to .json files.

format.py
This file combines json files and reduces to the variables used for training the model.

Models.ipynb 

Jupyter notebook used for building and training a ML model.  The current model takes top features from tfidf vectorizer from the Recipe Name, Description, Ingredient List, and Instructions.  These are then used to train a Random Forest Classifier in addition to the lengths associated with these secitons, (number of words in the recipe name, number of ingredients, etc.)

Graphs.ipynb
Jupyter notebook for generating the graphs used for the heroku website.  These graphs are made with altair.
