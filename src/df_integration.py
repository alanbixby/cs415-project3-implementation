import pandas as pd
from scipy.integrate import simpson

def df_int(df1: pd.DataFrame) -> float:
    return simpson(df1).sum()

def df_diff(df1: pd.DataFrame, df2: pd.DataFrame) -> float:
    return simpson(df1).sum() - simpson(df2).sum()