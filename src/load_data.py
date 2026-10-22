from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

#Todo lo de este archivo son celdas tomadas del notebook dentro de recicled y adapatadas como defs 
#para que jale algo biens
""""
activity_root = Path.cwd()
if activity_root.name == "notebooks":
    activity_root = activity_root.parent
dataset_root = activity_root / "data" / "SMSSpamCollection"
"""

def get_activity_root() -> Path:
    activity_root = Path.cwd()
    if activity_root.name == "notebooks":
        activity_root = activity_root.parent
    return activity_root


def load_dataset(path: Path | None = None) -> pd.DataFrame:
    if path is None:
        path = get_activity_root() / "data" / "SMSSpamCollection"
    if not path.is_file():
        raise FileNotFoundError()
    
    df = pd.read_csv(path, sep="\t", header=None, names=["label", "text"], encoding="utf-8")
    df["label"] = (df["label"] == "spam").astype(int)  
    # \0 ham y 1 es spam
    return df


def load(path: Path | None = None):

    messages = load_dataset(path)

    train_val, test_reviews = train_test_split(
        messages, test_size=0.15, random_state=42, stratify=messages["label"]
    )
    train_reviews, val_reviews = train_test_split(
        train_val, test_size=0.15 / 0.85, random_state=42, stratify=train_val["label"]
    )
    X_train = train_reviews["text"].copy()
    X_val = val_reviews["text"].copy()
    X_test = test_reviews["text"].copy()
    y_train = train_reviews["label"].copy()
    y_val = val_reviews["label"].copy()
    y_test = test_reviews["label"].copy()
    return X_train, X_val, X_test, y_train, y_val, y_test


if __name__ == "__main__":

    #Nomas para ver si si jalo
    X_train, X_val, X_test, y_train, y_val, y_test = load()
    print("Training:", len(X_train), "Validation:", len(X_val), "Test:", len(X_test))
    print("Training labels:", y_train.value_counts().sort_index().to_dict())
    print("Validation labels:", y_val.value_counts().sort_index().to_dict())
    print("Test labels:", y_test.value_counts().sort_index().to_dict())