import pandas as pd


def save_to_csv(item, file_name):
    df = pd.DataFrame([dict(item)])
    df.to_csv(file_name, mode="a", index=False, header=False)
