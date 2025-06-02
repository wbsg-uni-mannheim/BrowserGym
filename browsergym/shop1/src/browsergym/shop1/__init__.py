import os

from browsergym.core.registration import register_task

from . import all


def environment_variables_precheck():
    assert os.environ.get(
        "SHOP1_URL", None
    ), "Environment variable SHOP1_URL has not been setup."


ALL_SHOP1_TASKS = [

]

# register the Miniwob benchmark
for task in ALL_SHOP1_TASKS:
    register_task(
        task.get_task_id(),
        task,
        nondeterministic=task.nondeterministic,
    )
