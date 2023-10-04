from nowcast_lstm.LSTM import LSTM
from nowcast_lstm.model_selection import variable_selection, hyperparameter_tuning, select_model

### if the module is in a different directory
# import sys
# sys.path.append("path/containing/library/folder/")
from datathon.modelling_helper import min_max_scale_df

data = pd.read_csv("data/data.csv", parse_dates = ["date"])

target = "exports_usd"
train_start = "2019-01-01"
#validation_start = "2021-12-01"
test_start = "2023-01-01"

train = data.loc[lambda x: (x.date >= train_start) & (x.date < test_start), :].reset_index(drop = True)
unscaled_train = train.copy()
train = min_max_scale_df(train, unscaled_train)
test = data.loc[lambda x: (x.date >= train_start), :].reset_index(drop = True)
test = min_max_scale_df(test, unscaled_train)

chosen_model = select_model(
    data = train,
    target_variable = target,
    n_models = 5,
    n_timesteps_grid = [1],
    train_episodes_grid = [50, 100],
    batch_size_grid = [int(len(train)/2), int(len(train)/4)],
    n_hidden_grid = [10, 20, 40],
    n_layers_grid = [1, 2, 4],
    n_folds = 3,
    init_test_size = 0.5,
    initial_ordering = "feature_contribution"
)

print(chosen_model.variables.values[0])
print(chosen_model.hyperparameters.values[0])

# chosen hyperparams + variables
# ['crude_brent', 'vostochny', 'primorsk']
# {'n_models': 5, 'n_timesteps': 1, 'fill_na_func': <function nanmean at 0x00000208A9D86CA0>, 'fill_ragged_edges_func': <function nanmean at 0x00000208A9D86CA0>, 'train_episodes': 100, 'batch_size': 12, 'decay': 0.98, 'n_hidden': 40, 'n_layers': 2, 'dropout': 0, 'criterion': '', 'optimizer': '', 'optimizer_parameters': {'lr': 0.01}}

variables = chosen_model.variables.values[0]
model = LSTM(
    data = train.loc[:, ["date", target] + variables],
    target_variable = target,
    n_models = 20,
    n_timesteps = 1,
    train_episodes = 100,
    batch_size = 12,
    n_hidden = 40,
    n_layers = 2
)
model.train()

model.predict(test.loc[:, ["date", target] + variables]).set_index("date").plot()