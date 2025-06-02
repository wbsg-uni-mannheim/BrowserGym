from browsergym.core.registration import register_task

from . import all_task


ALL_WEBMALL_TASKS = []
for task in all_task:
    ALL_WEBMALL_TASKS.append(task)




# register the WebMall benchmark
for task in ALL_WEBMALL_TASKS:
    register_task(
        task.get_task_id(),
        task,
        nondeterministic=task.nondeterministic,
    )
