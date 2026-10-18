
# python -m src.train


import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline

from src.load_data import get_activity_root, load
from src.preprocessors import normalize_text


def main() -> None:

    activity_root = get_activity_root()
    models_dir = activity_root / "models"      
    model_path = models_dir / "spam_pipeline.joblib"

    X_train, X_val, X_test, y_train, y_val, y_test = load()
    print("Training:", len(X_train), "Validation:", len(X_val), "Test:", len(X_test))

    baseline_pipeline = Pipeline([
        ("vectorizer", CountVectorizer(preprocessor=normalize_text)),
        ("classifier", LogisticRegression(max_iter=1000)),
    ])
    alternative_1_pipeline = Pipeline([
        ("vectorizer", TfidfVectorizer(preprocessor=normalize_text)),
        ("classifier", LogisticRegression(max_iter=1000)),
    ])
    alternative_2_pipeline = Pipeline([
        ("vectorizer", CountVectorizer(preprocessor=normalize_text, ngram_range=(1, 2))),
        ("classifier", LogisticRegression(max_iter=1000)),
    ])

    names = ["baseline", "alternative_1", "alternative_2"]
    pipelines = [
        baseline_pipeline, alternative_1_pipeline, alternative_2_pipeline
    ]

    accuracies = []
    for name, pipeline in zip(names, pipelines):
        pipeline.fit(X_train, y_train)
        accuracies.append(accuracy_score(y_val, pipeline.predict(X_val)))

    results = pd.DataFrame({"pipeline": names, "accuracy": accuracies})
    print(results.assign(accuracy=results["accuracy"].map("{:.2%}".format)).to_string(index=False))

    bestIndex = accuracies.index(max(accuracies))
    best_name = names[bestIndex]
    best_pipeline = pipelines[bestIndex]
    print(f"Best pipeline: {best_name}")

    joblib.dump(best_pipeline, model_path)
    print("ruta:", model_path)


if __name__ == "__main__":
    main()