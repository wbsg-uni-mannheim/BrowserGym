from .task import WebMallTask

class SingleProductSearch(WebMallTask):
    def __init__(self):
        super().__init__(seed=1, task_id="Webmall_Single_Product_Search_Task1")