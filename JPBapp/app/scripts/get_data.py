import pandas as pd

def get_data(csv_path):
    data = pd.read_csv(csv_path)
    return data.to_json()