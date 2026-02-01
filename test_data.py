import pandas as pd

def test_no_nulls():
    df = pd.read_csv("clean_data.csv")
    assert df.isnull().sum().sum() == 0
