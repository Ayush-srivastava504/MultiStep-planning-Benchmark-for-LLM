import pandas as pd
import json
import yaml
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.evaluator import evaluate_batch, calculate_accuracy, evaluate_by_category
from src.utils import save_csv, save_json

def load_config():
    with open('configs/config.yaml', 'r') as f:
        return yaml.safe_load(f)

def simulate_model(question):
    import random
    question_lower = question.lower()
    
    if "add" in question_lower or "+" in question_lower:
        import re
        numbers = re.findall(r'\d+', question)
        if len(numbers) >= 2:
            return str(int(numbers[0]) + int(numbers[1]))
    
    if "ignore" in question_lower or "correction" in question_lower:
        import re
        numbers = re.findall(r'\d+', question)
        if numbers:
            return numbers[-1]
    
    if "subtract" in question_lower or "-" in question_lower:
        import re
        numbers = re.findall(r'\d+', question)
        if len(numbers) >= 2:
            return str(int(numbers[0]) - int(numbers[1]))
    
    if "multiply" in question_lower:
        import re
        numbers = re.findall(r'\d+', question)
        if len(numbers) >= 2:
            return str(int(numbers[0]) * int(numbers[1]))
    
    if "calculate" in question_lower:
        import re
        numbers = re.findall(r'\d+', question)
        if numbers:
            return str(sum(map(int, numbers)))
    
    return str(random.randint(1, 100))

def run_benchmark():
    config = load_config()
    
    df = pd.read_csv('data/raw/tasks.csv')
    
    predictions = []
    outputs = []
    
    for idx, row in df.iterrows():
        pred = simulate_model(row['question'])
        predictions.append(pred)
        outputs.append({
            'task_id': row['task_id'],
            'question': row['question'],
            'ground_truth': row['answer'],
            'prediction': pred,
            'task_type': row['task_type'],
            'difficulty': row['difficulty'],
            'trap_type': row['trap_type']
        })
    
    results = evaluate_batch(df['answer'].tolist(), predictions)
    accuracy = calculate_accuracy(results)
    
    df['correct'] = results
    
    type_accuracy = evaluate_by_category(df, results, 'task_type')
    difficulty_accuracy = evaluate_by_category(df, results, 'difficulty')
    trap_accuracy = evaluate_by_category(df, results, 'trap_type')
    
    metrics = {
        'model_name': config['model_name'],
        'overall_accuracy': accuracy,
        'total_tasks': len(df),
        'correct_tasks': sum(results),
        'accuracy_by_task_type': type_accuracy,
        'accuracy_by_difficulty': difficulty_accuracy,
        'accuracy_by_trap_type': trap_accuracy
    }
    
    metrics_df = pd.DataFrame([metrics])
    save_csv(metrics_df, 'results/metrics.csv')
    save_json(outputs, 'results/outputs.json')
    
    print(f"Benchmark completed. Overall accuracy: {accuracy:.2%}")
    
    return metrics, outputs

if __name__ == "__main__":
    run_benchmark()