from browsergym.core.registration import register_task
import gymnasium as gym
from .task import WebMallTask

import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class WebMallTaskInstance(WebMallTask):
    def __init__(self, task_id: str, seed: int = None):
        super().__init__(seed=seed, task_id=task_id)


# --- Load all task IDs from task_sets.json ---
task_sets_path = Path(__file__).parent / "task_sets.json"

with task_sets_path.open() as f:
    task_sets = json.load(f)

TASK_IDS = []
for task_set in task_sets:
    for task in task_set.get("tasks", []):
        TASK_IDS.append(f"webmall.{task['id']}")

for tid in TASK_IDS:
    register_task(
        id=tid,
        task_class=WebMallTaskInstance,
        task_kwargs={"task_id": tid},  # passed to __init__
        nondeterministic=True,
    )