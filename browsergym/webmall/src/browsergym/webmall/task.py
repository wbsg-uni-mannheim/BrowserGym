import os
import logging
import json

from typing import Tuple
from playwright.sync_api import Page
from pathlib import Path
from evaluator import Evaluator, StringEvaluator, HTMLEvaluator, URLEvaluator, EvaluatorComb

logger = logging.getLogger(__name__)

from browsergym.core.task import AbstractBrowserTask


class WebMallTask(AbstractBrowserTask):

    @classmethod
    def get_task_id(cls) -> str:
        """
        Generic class for several task ids, this way of obtaining the task id is not compatible for now.
        """
        raise NotImplementedError

    def __init__(
        self, seed: int, task_id: str, output_file: str = None, save_predictions: bool = False
    ) -> None:
        """
        Args:
            seed (int): Random seed for task initialization.
            task_id (str): Unique identifier for the task (for the BrowserGym environment).
            output_file (str, optional): Path to the output file for saving results, needed for test set.
            save_predictions (bool, optional): Save predictions to the output file (yes/no).
        """
        super().__init__(seed)
        self.task_id = task_id
        self.start_url = "http://localhost:80"

        json_path = Path(__file__).parent / "task_sets.json"
        self.task_sets = json.load(json_path)

        self.task_config = _get_task(task_id)


    def setup(self, page: Page) -> Tuple[str, dict]:
        logger.info(f"Navigating to start url: {self.start_url}")
        page.goto(self.start_url, timeout=10000)
        
        return self.task_config.get("instruction"), {}

    def teardown(self) -> None:
        pass

    def validate(self, page: Page, chat_messages: list[dict]) -> Tuple[float, bool, str, dict]:
        # if any, use the last assistant message as the stop answer for webarena
        if chat_messages and chat_messages[-1]["role"] == "assistant":
            last_action = {"answer": chat_messages[-1]["message"]}
        elif chat_messages and chat_messages[-1]["role"] == "infeasible":
            last_action = {"answer": "N/A"}
        else:
            last_action = {"answer": ""}

        # # hack: fake trajectory for evaluation (only last_action["answer"] is used in the webarena evaluation codebase)
        # trajectory = [{}, last_action]  # StateInfo, Action

        # # call the evaluator
        # try:
        #     score = self.evaluator(
        #         trajectory=trajectory,
        #         config_file=self.config_file,
        #         page=page,
        #         client=None,  # none of webarena's evaluators requires a cdp session
        #     )


        # TODO: build some evaluator class that evaluates score and stopping criterion based on task config, current page and chat messages
        evaluator = _evaluator_router(self.task_config)
        trajectory = [{}, last_action]  # StateInfo, Action
        score = evaluator.score(trajectory)
        if chat_messages and chat_messages[-1]["role"] == "assistant":    
            if score > 0:
                return score, True, "", {}
            else:
                return score, False, "", {}
        elif chat_messages and chat_messages[-1]["role"] == "infeasible":
            return score, True, "", {}


def _get_task(data: dict, target_id: str) -> dict | None:
    """
    Returns a specific task from the task set.
    """
    for task_set in data.get("task_sets", []):
        for task in task_set.get("tasks", []):
            if task.get("id") == target_id:
                return task
    return None


def _evaluator_router(task_config: dict) -> EvaluatorComb:
    """Router to get the evaluator class"""
    eval_types = [task_config["correct_answer"]["type"]]
    correct_answers = task_config["correct_answer"]["answers"]
    evaluators: list[Evaluator] = []
    for eval_type in eval_types:
        match eval_type:
            case "string_match":
                evaluators.append(StringEvaluator(correct_answers))
            case "url_match":
                evaluators.append(URLEvaluator(correct_answers))
            case "program_html":
                evaluators.append(HTMLEvaluator(correct_answers))
            case _:
                raise ValueError(f"eval_type {eval_type} is not supported")

    return EvaluatorComb(evaluators)