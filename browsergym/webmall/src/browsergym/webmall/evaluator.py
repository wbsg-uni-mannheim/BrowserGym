from playwright.sync_api import Page

class Evaluator():
    def __init__(self, correct_answers: list):
        self.correct_answers = correct_answers


class StringEvaluator(Evaluator):
    def __init__(self, correct_answers):
        super().__init__(correct_answers)

    def eval(self, trajectory, page: Page):
        return 1

class HTMLEvaluator(Evaluator):
    def __init__(self, correct_answers):
        super().__init__(correct_answers)

    def eval(self, trajectory, page: Page):
        return 1

class URLEvaluator(Evaluator):
    def __init__(self, correct_answers):
        super().__init__(correct_answers)

    def eval(self, trajectory, page: Page):
        return 1

class EvaluatorComb():
    def __init__(self, evaluators: list[Evaluator]):
        self.evaluators = evaluators

    def eval(self, trajectory, page: Page):
        score = 1
        for evaluator in self.evaluators:
            score += evaluator.eval(trajectory, page)
        return score







