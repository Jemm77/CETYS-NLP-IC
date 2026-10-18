
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline

from src.load_data import get_activity_root, load
from src.preprocessors import normalize_text

#para correr usar 'python -m src.tfidf's  
def main() -> None:
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
        baseline_pipeline, alternative_1_pipeline, alternative_2_pipeline,
    ]


    accuracies = []
    for name, pipeline in zip(names, pipelines):
        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_val)
        accuracies.append(accuracy_score(y_val, predictions))

    results = pd.DataFrame({"pipeline": names, "accuracy": accuracies})
    print(results.assign(accuracy=results["accuracy"].map("{:.2%}".format)).to_string(index=False))

    bestIndex = accuracies.index(max(accuracies))
    best_name = names[bestIndex]
    best_pipeline = pipelines[bestIndex]
    print(f"Best pipeline: {best_name}")

if __name__ == "__main__":
    main()
