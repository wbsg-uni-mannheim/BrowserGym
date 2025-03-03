from playwright.sync_api import Page
from bs4 import BeautifulSoup

class Evaluator():
    def __init__(self, correct_answer: dict):
        self.correct_answer = correct_answer


class StringEvaluator(Evaluator):
    def __init__(self, correct_answer):
        super().__init__(correct_answer)

    def eval(self, trajectory, page: Page):
        return 0

class HTMLEvaluator(Evaluator):
    def __init__(self, correct_answer):
        super().__init__(correct_answer)

    def eval(self, trajectory, page: Page):
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        for a in self.correct_answer.get("answers"):
            html_element_class = a.get("element_class")
            found = any(a.get("answer") in message.get_text(strip=True) for message in soup.find_all("div", class_=html_element_class))
            if found:
                break

        if found:
            return 1
        else:
            return 0

class URLEvaluator(Evaluator):
    def __init__(self, correct_answer):
        super().__init__(correct_answer)

    def eval(self, trajectory, page: Page):
        print(f"Evaluating URL: {page.url}")
        if page.url in self.correct_answer.get("answers"):
            return 1
        else:
            return 0

class EvaluatorComb():
    def __init__(self, evaluators: list[Evaluator]):
        self.evaluators = evaluators

    def score(self, trajectory, page: Page):
        score = 0
        for evaluator in self.evaluators:
            score += evaluator.eval(trajectory, page)
        return score







