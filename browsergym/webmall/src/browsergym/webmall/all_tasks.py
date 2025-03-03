from .task import WebMallTask

class SingleProductSearch(WebMallTask):
    def __init__(self, seed: int = None):
        super().__init__(seed=seed, task_id="Webmall_Single_Product_Search_Task1")


all_tasks = [SingleProductSearch]