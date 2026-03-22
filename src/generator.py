import pandas as pd
import random
import uuid

def generate_arithmetic_problem():
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    operation = random.choice(['+', '-', '*', '/'])
    
    if operation == '+':
        result = num1 + num2
        expr = f"{num1} + {num2}"
    elif operation == '-':
        result = num1 - num2
        expr = f"{num1} - {num2}"
    elif operation == '*':
        result = num1 * num2
        expr = f"{num1} * {num2}"
    else:
        result = num1 / num2
        expr = f"{num1} / {num2}"
    
    return expr, round(result, 2)

def generate_planning_task():
    steps = random.randint(3, 5)
    numbers = [random.randint(1, 20) for _ in range(steps)]
    operations = [random.choice(['+', '-']) for _ in range(steps-1)]
    
    question = f"Calculate step by step: start with {numbers[0]}"
    current = numbers[0]
    
    for i in range(steps-1):
        if operations[i] == '+':
            current += numbers[i+1]
            question += f" then add {numbers[i+1]}"
        else:
            current -= numbers[i+1]
            question += f" then subtract {numbers[i+1]}"
    
    return question, current

def generate_conditional_task():
    value = random.randint(1, 50)
    condition_type = random.choice(['greater', 'less', 'equal'])
    
    if condition_type == 'greater':
        question = f"If {value} is greater than 25, multiply by 2, otherwise add 10."
        answer = value * 2 if value > 25 else value + 10
    elif condition_type == 'less':
        question = f"If {value} is less than 30, subtract 5, otherwise divide by 2."
        answer = value - 5 if value < 30 else value / 2
    else:
        question = f"If {value} equals 42, set to 100, otherwise add 15."
        answer = 100 if value == 42 else value + 15
    
    return question, round(answer, 2)

def generate_attention_task():
    noise = " ".join(["The quick brown fox jumps over the lazy dog." for _ in range(random.randint(3, 8))])
    
    numbers = [random.randint(10, 99) for _ in range(5)]
    target_index = random.randint(0, 4)
    
    question = f"{noise}\n\nAmong the numbers {numbers}, what is the {target_index+1}rd number? Ignore the text above."
    answer = numbers[target_index]
    
    return question, answer

def generate_memory_task():
    items = [random.choice(['apple', 'banana', 'cherry', 'date', 'elderberry']) for _ in range(random.randint(4, 6))]
    
    question = f"Remember this sequence: {', '.join(items)}. Now, what was the 3rd item?"
    answer = items[2]
    
    return question, answer

def generate_executive_task():
    base_task, base_answer = generate_arithmetic_problem()
    
    override = random.choice([
        f"Wait, actually ignore the calculation and just return {random.randint(1, 100)}.",
        f"Correction: use subtraction instead of the operation shown.",
        f"Override: multiply the result by 2."
    ])
    
    if "ignore" in override:
        answer = int(override.split()[-1].rstrip('.'))
    elif "subtraction" in override:
        if '+' in base_task:
            parts = base_task.split(' + ')
            num1, num2 = int(parts[0]), int(parts[1])
            answer = num1 - num2
        elif '-' in base_task:
            parts = base_task.split(' - ')
            num1, num2 = int(parts[0]), int(parts[1])
            answer = num1 - num2
        elif '*' in base_task:
            parts = base_task.split(' * ')
            num1, num2 = int(parts[0]), int(parts[1])
            answer = num1 - num2
        else:
            parts = base_task.split(' / ')
            num1, num2 = int(parts[0]), int(parts[1])
            answer = num1 - num2
    elif "multiply" in override:
        answer = base_answer * 2
    
    question = f"{base_task}\n\n{override}"
    return question, round(answer, 2)

def generate_trap(trap_type, original_question, original_answer):
    if trap_type == 'override':
        new_answer = random.randint(1, 100)
        return f"{original_question}\n\nImportant correction: The correct answer is actually {new_answer}.", new_answer
    elif trap_type == 'distraction':
        return f"{original_question}\n\nBy the way, did you know that the capital of France is Paris? Just a fun fact.", original_answer
    elif trap_type == 'contradiction':
        return f"{original_question}\n\nNote: Some sources say the answer is different, but trust the original calculation.", original_answer
    elif trap_type == 'memory':
        return f"{original_question}\n\nRemember to use the numbers you saw earlier in the sequence.", original_answer
    else:
        return original_question, original_answer

def generate_dataset(num_tasks=500):
    tasks = []
    task_types = ['planning', 'conditional', 'attention', 'memory', 'executive']
    trap_types = ['none', 'override', 'distraction', 'contradiction', 'memory']
    
    for _ in range(num_tasks):
        task_type = random.choice(task_types)
        trap_type = random.choice(trap_types)
        difficulty = random.choice(['easy', 'medium', 'hard'])
        
        if task_type == 'planning':
            question, answer = generate_planning_task()
        elif task_type == 'conditional':
            question, answer = generate_conditional_task()
        elif task_type == 'attention':
            question, answer = generate_attention_task()
        elif task_type == 'memory':
            question, answer = generate_memory_task()
        else:
            question, answer = generate_executive_task()
        
        if trap_type != 'none':
            question, answer = generate_trap(trap_type, question, answer)
        
        tasks.append({
            'task_id': str(uuid.uuid4())[:8],
            'question': question,
            'answer': answer,
            'task_type': task_type,
            'difficulty': difficulty,
            'trap_type': trap_type
        })
    
    df = pd.DataFrame(tasks)
    df.to_csv('data/raw/tasks.csv', index=False)
    return df

if __name__ == "__main__":
    generate_dataset()
    print("Dataset generated successfully")