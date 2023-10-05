
# 2023 UN Datathon Day 2 Workshop
## Task
The workshop task is to use the AIS and World Bank data gathered yesterday to create a machine learning model to get predictions for Russian exports in USD for the latest available months.

Try to apply the principles and practices discussed in the presentation earlier. That means try to:

- create the model in Python, though you can create an OLS model in Excel
- use [sci-kit learn](https://scikit-learn.org/) or [nowcast_lstm](https://github.com/dhopp1/nowcast_lstm)  and their many in-built functions for cross-validation, hyperparameter tuning, etc.

## Steps
1.  Use the code you developed yesterday to get the data. The data is also available directly in this repository if you would like to focus on the modelling.
2. Process the data so that it is suitable for use in a machine learning model
3. Select a methodology and hyperparameter tune to obtain a final model. Some suitable options are:
	- [Gradient Boost](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html)
	- [LSTMs](https://github.com/dhopp1/nowcast_lstm)
	- [OLS](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
	- [Random Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)

4. Visualize your model's predictions somehow
5. Save your model's predictions for the latest month

## What this repository does
- This repository accomplishes the task by running the `modelling_sklearn.py` and `modelling_lstm.py` files. You can follow the code for more information, but in essence they perform the same task just for the syntax of `sklearn` and `nowcast_lstm`. They:
	- read the data and min-max scale it to make it suitable for the algorithms
	- perform model selection on the training set
	- train a final model with the chosen hyperparameters
	- output a plot of the models' predictions
	- output a CSV of the models' predictions