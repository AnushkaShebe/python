from pathlib import Path
import pandas as pd
from config import HISTORY_FILE

def save_record(record):
    path = Path(HISTORY_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    new_df = pd.DataFrame([record])

    if path.exists():
        old_df = pd.read_csv(path)
        df = pd.concat([old_df, new_df], ignore_index=True)
    else:
        df = new_df

    df.to_csv(path, index=False)

def load_history():
    path = Path(HISTORY_FILE)
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)
