import pandas as pd

def min_max_scale_df(df, reference_df, unscale = False):
    """
    Min-max scale a dataframe
    parameters:
        :df: pd.DataFrame: the dataframe to min-max scale according to the reference dataframe. The first column will not be scaled (i.e., the date)
        :reference_df: pd.DataFrame: the reference dataframe to compute min and maxes (e.g., the training data)
        :unscale: bool: False to min max scale, True to rescale to original units
    output:
        :pd.DataFrame: min-max scaled dataframe
    """    
    scaled_df = df.copy()
    if not(unscale):
        for col in df.columns[1:]:
            scaled_df[col] = (df[col] - reference_df[col].min()) / (reference_df[col].max() - reference_df[col].min())
    else:
        for col in df.columns[1:]:
            scaled_df[col] = (df[col] * (reference_df[col].max() - reference_df[col].min())) + reference_df[col].min()
        
    return scaled_df