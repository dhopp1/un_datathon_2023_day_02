import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV

### if the module is in a different directory
# import sys
# sys.path.append("path/containing/library/folder/")
from datathon.modelling_helper import min_max_scale_df

# data setup
data = pd.read_csv("data/data.csv", parse_dates = ["date"])

# the name of the target variable
target = "exports_usd"

# The dates for the train and test set
train_start = "2019-01-01"
test_start = "2023-01-01"

train = data.loc[lambda x: (x.date >= train_start) & (x.date < test_start), :].reset_index(drop = True)
unscaled_train = train.copy() # preserve the unscaled data to be able to unscale
train = min_max_scale_df(train, unscaled_train) # min-max scaling the training data
test = data.copy()
test = min_max_scale_df(test, unscaled_train)

# set to true if performing model selection
if False:
    
    # create a train and test set for assessing the chosen model
    X_train, X_test, y_train, y_test = train_test_split(train.drop(["date", target], axis = 1), train[target], test_size=0.2, random_state = 0)
    
    # creating modelling pipeline
    model = RandomForestRegressor()
    cv = KFold(n_splits = 10, random_state = 0, shuffle = True) # use 10-fold cross validation
    
    # the hyperparameters to check
    search_space = {
        "n_estimators": [50, 100],
        "max_depth": [None, 3, 6],
        "min_samples_split": [2, 0.01],
        "min_samples_leaf": [1, 0.01],
        "max_features": [1, "sqrt", 0.8]
    }
    
    # create the grid search object
    search = GridSearchCV(estimator = model, param_grid = search_space, scoring = "neg_mean_squared_error", n_jobs = -1, cv = cv)
    
    # perform the search
    result = search.fit(X_train, y_train)
    print(result.best_estimator_)
    
    # check the performance of the best-performing model
    model = result.best_estimator_
    model.fit(X_train, y_train)
    
# model inference
# instantiate the model with the chosen hyperparameters
model = RandomForestRegressor(
    n_estimators = 50,
    max_depth = 6,
    max_features = 0.8,
    min_samples_leaf = 0.01,
)
model.fit(train.drop(["date", target], axis = 1), train[target])

# unscaling - get results in the original unit of the target variable
preds = model.predict(test.drop(["date", target], axis = 1))
preds = pd.DataFrame({
    "date": test.date,
    "predictions": preds
})
unscaled_actuals = test.copy()
unscaled_actuals = min_max_scale_df(test, unscaled_train, unscale = True)
unscaled_preds = test.copy()
unscaled_preds = unscaled_preds.drop(target, axis = 1).merge(preds, on = "date", how = "left").rename(columns = {"predictions": target})
unscaled_preds = min_max_scale_df(unscaled_preds, unscaled_train, unscale = True)

# plotting and writing out the predictions
final_df = pd.DataFrame({
    "date": unscaled_actuals.date,
    "actuals": unscaled_actuals[target],
    "predictions": unscaled_preds[target]
})

final_df.to_csv("rf_predictions.csv", index = False)

final_df.set_index("date").plot()
plt.axvline(pd.to_datetime(test_start))
plt.savefig("rf_plot.png")