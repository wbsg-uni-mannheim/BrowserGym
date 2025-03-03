from browsergym.core.registration import register_task

from .all_tasks import all_tasks


ALL_WEBMALL_TASKS = [task for task in all_tasks]

print("Starting registration process")



# register the WebMall benchmark
for task in ALL_WEBMALL_TASKS:
    print(f"Registering WebMall task: {task().get_task_id()}")
    register_task(
        task().get_task_id(),
        task,
        nondeterministic=True,
    )
