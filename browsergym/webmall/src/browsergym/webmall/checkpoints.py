from dataclasses import dataclass, asdict
from collections import defaultdict
from typing import List, Dict, Any

@dataclass
class Checkpoint:
    id: str
    value: str
    type: str  # "string", "cart", "checkout"
    flag: bool = False
    weight: float = 1.0

@dataclass
class CheckoutCheckpoint(Checkpoint):
    user_details: Dict[str, Any] = None  # e.g. {"first_name": "...", ...}
    payment_info: Dict[str, Any] = None  # {"method": "Cash on delivery"} or {"method": "Check payments"}

class Checklist:
    def __init__(self, task_config: dict, task_id: str = "", urls: dict = None):
        self.checkpoints: List[Checkpoint] = []
        answers = task_config["correct_answer"]["answers"]
        answer_type = task_config["correct_answer"].get("type", "string")

        # --- Step 1: Group checkpoints ---
        answer_cps = []
        cart_cps = []  # Will move into product_page_cps if answer_type == "checkout"
        product_page_cps = []

        # --- Step 2: Process answer checkpoints ---
        checkout_answer = None
        for i, answer in enumerate(answers, 1):
            if answer_type == "checkout":
                # Add checkout checkpoint to correct answer group
                answer_cps.append(CheckoutCheckpoint(
                    id="answer" + str(i),
                    value=answer,
                    type="checkout",
                    user_details=task_config.get("user_details"),
                    payment_info=task_config.get("payment_info"),
                ))
                checkout_answer = answer
                # Cart goes into product_page_cps
                cart_cps.append(Checkpoint(id="cart" + str(i), value=answer, type="cart"))
            else:
                answer_cps.append(Checkpoint(id="answer" + str(i), value=answer, type=answer_type))
            
            # Checkpoints for product page visits
            product_url = answer
            checkpoint_id = f"visit_product_page_{i}"
            product_page_cps.append(Checkpoint(id=checkpoint_id, value=product_url, type="url"))
        
        # Add cart checkpoints (if any) to product_page group
        product_page_cps.extend(cart_cps)

        # --- Step 3: Normalize weights ---

        # (1) Correct answers → 0.8
        if answer_cps:
            for cp in answer_cps:
                cp.weight = 0.8 / len(answer_cps)
        self.checkpoints.extend(answer_cps)

        # (2) Product page group → 0.2
        if product_page_cps:
            for cp in product_page_cps:
                cp.weight = 0.2 / len(product_page_cps)
        self.checkpoints.extend(product_page_cps)


    def group_by_type(self):
        grouped = defaultdict(list)
        for cp in self.checkpoints:
            grouped[cp.type].append(cp)
        return grouped

    def total_score(self):
        return sum(cp.weight for cp in self.checkpoints if cp.flag)

    def all_completed(self) -> bool:
        return all(cp.flag for cp in self.checkpoints)
    
    def get_unchecked_checkpoints(self):
        return [cp for cp in self.checkpoints if not cp.flag]
    
    def get_checked_checkpoints(self):
        return [cp for cp in self.checkpoints if cp.flag]
    
    def get_unchecked_dict(self):
        return [asdict(cp) for cp in self.checkpoints if not cp.flag]
    
    def get_checked_dict(self):
        return [asdict(cp) for cp in self.checkpoints if cp.flag]

    def get_checklist_dict(self):
        return [asdict(cp) for cp in self.checkpoints]