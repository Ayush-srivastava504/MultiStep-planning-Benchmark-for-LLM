import pandas as pd

def evaluate_prediction(ground_truth, prediction):
    if isinstance(ground_truth, (int, float)):
        try:
            pred_value = float(prediction) if isinstance(prediction, str) else prediction
            return abs(ground_truth - pred_value) < 0.01
        except:
            return False
    else:
        return str(ground_truth).strip().lower() == str(prediction).strip().lower()

def evaluate_batch(ground_truths, predictions):
    results = []
    for gt, pred in zip(ground_truths, predictions):
        results.append(evaluate_prediction(gt, pred))
    return results

def calculate_accuracy(results):
    return sum(results) / len(results) if results else 0.0

def evaluate_by_category(df, results, category):
    category_results = {}
    for cat in df[category].unique():
        mask = df[category] == cat
        cat_results = [r for i, r in enumerate(results) if mask.iloc[i]]
        if cat_results:
            category_results[cat] = calculate_accuracy(cat_results)
    return category_results