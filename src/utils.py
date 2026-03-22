import json
import pandas as pd

def format_answer(answer):
    if isinstance(answer, float):
        return round(answer, 2)
    return answer

def parse_numeric_answer(answer_str):
    try:
        return float(answer_str.strip())
    except:
        return None

def save_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def save_csv(df, filepath):
    df.to_csv(filepath, index=False)

def load_csv(filepath):
    return pd.read_csv(filepath)