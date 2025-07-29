import json
import csv

# Replace these paths with your actual file paths
json_path = 'task_sets.json'
csv_path = '../experiments/src/browsergym/experiments/benchmark/metadata/webmall.csv'

# Fixed values for the CSV
requires_reset = 'False'
sites = 'shopping_admin'
eval_types = 'string_match'
task_id = '0'
browsergym_split = 'train'
depends_on = ''

# Open and load the JSON file
with open(json_path, 'r') as f:
    task_sets = json.load(f)

# Prepare the CSV header
header = [
    'task_name', 'requires_reset', 'sites', 'eval_types', 'task_id', 'browsergym_split', 'depends_on'
]

# Open the CSV file and write rows
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for task_set in task_sets:
        tasks = task_set.get('tasks', [])
        for task in tasks:
            task_name = f"webmall.{task['id']}"
            row = [
                task_name,
                requires_reset,
                sites,
                eval_types,
                task_id,
                browsergym_split,
                depends_on
            ]
            print(row)
            writer.writerow(row)

print(f"CSV file has been created at {csv_path}")