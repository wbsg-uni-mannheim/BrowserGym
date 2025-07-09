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
                cart_cps.append(Checkpoint(id="answer" + str(i), value=answer, type="cart"))
            else:
                answer_cps.append(Checkpoint(id="answer" + str(i), value=answer, type=answer_type))

        # --- Step 3: Normalize weights ---

        # (1) Correct answers → 0.5
        if answer_cps:
            for cp in answer_cps:
                cp.weight = 0.5 / len(answer_cps)
        self.checkpoints.extend(answer_cps)

        # (2) Visiting each shop → 0.2
        shop_visit_cps = [
            Checkpoint(id="visit_shop1", value=urls["SHOP1_URL"], type="url"),
            Checkpoint(id="visit_shop2", value=urls["SHOP2_URL"], type="url"),
            Checkpoint(id="visit_shop3", value=urls["SHOP3_URL"], type="url"),
            Checkpoint(id="visit_shop4", value=urls["SHOP4_URL"], type="url"),
        ]

        # For checkout task: only need to visit single shop
        if checkout_answer is not None:
            shop_visit_cps = [cp for cp in shop_visit_cps if getattr(cp, "value", None) in checkout_answer]
 
        for cp in shop_visit_cps:
            cp.weight = 0.2 / len(shop_visit_cps)
        self.checkpoints.extend(shop_visit_cps)

        # (3) Product page visits (task_config + cart if checkout)
        for shop_key, offers in task_config["relevant_offers"].items():
            for offer in offers:
                if "product_url" in offer:
                    product_url = offer["product_url"].replace("http://localhost:SHOP1_PORT", urls["SHOP1_URL"]) \
                                                    .replace("http://localhost:SHOP2_PORT", urls["SHOP2_URL"]) \
                                                    .replace("http://localhost:SHOP3_PORT", urls["SHOP3_URL"]) \
                                                    .replace("http://localhost:SHOP4_PORT", urls["SHOP4_URL"])
                    checkpoint_id = f"visit_product_{offer['webmall_id']}"
                    product_page_cps.append(Checkpoint(id=checkpoint_id, value=product_url, type="url"))

        # Add cart checkpoints (if any) to product_page group
        product_page_cps.extend(cart_cps)

        # Assign weight: product page group → 0.3
        if product_page_cps:
            for cp in product_page_cps:
                cp.weight = 0.3 / len(product_page_cps)
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