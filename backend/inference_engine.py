"""
File: inference_engine_v4.py
Description: Forward-chaining inference engine for military service consultation system.
             This module implements a rule-based expert system that evaluates citizen eligibility
             for military service based on Vietnamese military service law (Luật Nghĩa vụ quân sự 2015).
             The engine processes rules from a JSON knowledge base and performs forward-chaining inference
             to determine if a citizen is eligible, exempt, or deferred from military service.
Version: 4.0
"""

import json

class InferenceEngine:
    def __init__(self, rules_file_path):
        """
        TASK: Knowledge Base Initialization
        
        Loads the rule-based knowledge base from a JSON file and prepares it for inference.
        Rules are automatically sorted by priority (higher priority rules execute first).
        
        Args:
            rules_file_path (str): Path to the JSON file containing the knowledge base rules.
        
        Returns:
            None. Rules are stored in self.rules as a sorted list.
        """
        print(f"Loading Knowledge Base from: {rules_file_path}")
        try:
            with open(rules_file_path, 'r', encoding='utf-8') as f:
                rules_data = json.load(f)['rules']
            
            # RULE SORTING: reverse=True -> 100 (Volunteer) runs first, -100 (Final Compilation) runs last
            self.rules = sorted(
                rules_data, 
                key=lambda r: r.get('priority', 0), 
                reverse=True
            )
            print(f"Loaded and sorted {len(self.rules)} rules.")
        
        except FileNotFoundError:
            print(f"ERROR: Knowledge Base file not found at: {rules_file_path}")
            self.rules = []
        except Exception as e:
            print(f"ERROR: Cannot read Knowledge Base file. Error: {e}")
            self.rules = []

    def _check_condition(self, fact_value, operator, rule_value):
        """
        TASK: Condition Matching (Atomic Level)
        
        Evaluates a single condition by comparing a fact value against a rule value using
        the specified operator. Handles None values correctly to prevent runtime errors.
        
        Args:
            fact_value: The current value of a fact from the working memory (can be None).
            operator (str): Comparison operator (==, !=, >, >=, <, <=, IN).
            rule_value: The target value specified in the rule condition.
        
        Returns:
            bool: True if the condition is satisfied, False otherwise.
        """
        
        # Handle when fact (fact_value) doesn't exist yet (is None)
        if fact_value is None:
            if operator == '==':
                return rule_value is None
            if operator == '!=':
                return rule_value is not None
            return False

        # Handle when rule value (rule_value) is None
        if rule_value is None:
            if operator == '==':
                return fact_value is None
            if operator == '!=':
                return fact_value is not None
            return False

        # Comparison operators (when both are not None)
        if operator == '==':
            return fact_value == rule_value
        if operator == '!=':
            return fact_value != rule_value
        if operator == '>':
            return fact_value > rule_value
        if operator == '>=':
            return fact_value >= rule_value
        if operator == '<':
            return fact_value < rule_value
        if operator == '<=':
            return fact_value <= rule_value
        if operator == 'IN':
            return fact_value in rule_value
        
        print(f"Error: Unrecognized operator '{operator}'")
        return False

    def _evaluate_rule(self, rule, known_facts):
        """
        TASK: Rule Evaluation (Complete Rule Level)
        
        Determines if a rule can be fired by evaluating all its preconditions and conditions.
        Supports both AND and OR logical operators for combining multiple conditions.
        
        Args:
            rule (dict): A rule object containing conditions, preconditions, and actions.
            known_facts (dict): Current working memory containing all known facts.
        
        Returns:
            bool: True if all preconditions and conditions are satisfied, False otherwise.
        """
        if 'pre_conditions' in rule:
            for pre_cond in rule['pre_conditions']:
                fact_value = known_facts.get(pre_cond['fact'])
                if not self._check_condition(fact_value, pre_cond['operator'], pre_cond['value']):
                    return False

        operator_type = rule.get('conditions_operator', 'AND')

        if operator_type == 'AND':
            for cond in rule['conditions']:
                fact_value = known_facts.get(cond['fact'])
                if not self._check_condition(fact_value, cond['operator'], cond['value']):
                    return False
            return True

        elif operator_type == 'OR':
            for cond in rule['conditions']:
                fact_value = known_facts.get(cond['fact'])
                if self._check_condition(fact_value, cond['operator'], cond['value']):
                    return True
            return False
            
        return False

    def _compile_final_result(self, known_facts):
        """
        TASK: Final Conclusion Compilation
        
        Synthesizes all intermediate conclusions into a final verdict about military service eligibility.
        Examines the list of reasons (failures, exemptions, deferrals) collected during inference
        and produces a human-readable conclusion with explanation.
        
        Args:
            known_facts (dict): Working memory containing all facts and intermediate conclusions.
        
        Returns:
            None. Updates known_facts with "KET_LUAN" (conclusion) and "GIAI_THICH" (explanation).
        """
        # Get list of reasons. If doesn't exist, default to empty list
        reasons = known_facts.get("LY_DO_TONG_HOP", [])
        is_volunteer = known_facts.get("tinh_nguyen_nhap_ngu", False)

        # Logic xử lý Tình nguyện:
        # Nếu tình nguyện, chỉ được bỏ qua các lý do về "Tạm hoãn" hoặc "Miễn".
        # Vẫn phải đạt tiêu chuẩn về Tuổi, Sức khỏe, Văn hóa.
        if is_volunteer:
            # Lọc bỏ các lý do tạm hoãn/miễn
            filtered_reasons = [
                r for r in reasons 
                if r not in ["Thuộc trường hợp miễn", "Thuộc trường hợp tạm hoãn"]
            ]
            
            if len(filtered_reasons) == 0:
                # Nếu sau khi lọc mà hết lý do -> Đủ điều kiện
                known_facts["KET_LUAN"] = "ĐỦ ĐIỀU KIỆN GỌI NHẬP NGŨ (Tình nguyện)"
                known_facts["GIAI_THICH"] = "Công dân tình nguyện nhập ngũ (được ưu tiên xét tuyển dù thuộc diện Tạm hoãn/Miễn)."
                return
            else:
                # Nếu vẫn còn lý do (VD: Sức khỏe, Tuổi) -> Vẫn không đạt
                reasons = filtered_reasons
        
        if len(reasons) == 0:
            known_facts["KET_LUAN"] = "ĐỦ ĐIỀU KIỆN GỌI NHẬP NGŨ"
            known_facts["GIAI_THICH"] = "Đạt các tiêu chuẩn về Tuổi, Sức khỏe và Văn hóa."
        else:
            unique_reasons = list(dict.fromkeys(reasons))
            reason_str = ", ".join(unique_reasons)
            
            known_facts["KET_LUAN"] = "KHÔNG ĐỦ ĐIỀU KIỆN GỌI NHẬP NGŨ"
            known_facts["GIAI_THICH"] = "Lý do: " + reason_str + "."

    def evaluate(self, initial_facts):
        """
        TASK: Forward-Chaining Inference Engine
        
        Main inference loop that applies rules iteratively until no new facts can be derived.
        Uses forward-chaining algorithm to propagate facts through the knowledge base.
        Supports priority-based rule execution and early stopping for volunteer cases.
        
        Args:
            initial_facts (dict): Input facts about a citizen (age, health, education, etc.).
        
        Returns:
            tuple: (conclusion, explanation, trace)
                - conclusion (str): Final verdict (eligible/not eligible).
                - explanation (str): Human-readable explanation of the conclusion.
                - trace (dict): Dictionary of all fired rules for audit trail.
        """
        
        # Initialize
        known_facts = initial_facts.copy()
        known_facts["KET_LUAN"] = "Không thể đưa ra kết luận"
        known_facts["GIAI_THICH"] = "Không có luật nào phù hợp"
        known_facts["LY_DO_TONG_HOP"] = []
        
        solution_trace = {}
        new_facts_found = True

        print("--- [IE] Starting forward chaining inference... ---")
        
        while new_facts_found:
            new_facts_found = False
            
            for rule in self.rules:
                if rule['id'] not in solution_trace:
                    if self._evaluate_rule(rule, known_facts):
                        
                        print(f"    -> [IE] Rule triggered: {rule['id']} ({rule['description']})")
                        new_facts_found = True
                        solution_trace[rule['id']] = rule

                        for action in rule['actions']:
                            fact_name = action['fact']
                            
                            # Check special action: COMPILE_FINAL_RESULT
                            if fact_name == "COMPILE_FINAL_RESULT":
                                self._compile_final_result(known_facts)
                            
                            elif 'add_to_list' in action:
                                value_to_add = action['add_to_list']
                                if value_to_add not in known_facts["LY_DO_TONG_HOP"]:
                                    known_facts["LY_DO_TONG_HOP"].append(value_to_add)
                            
                            elif 'value' in action:
                                known_facts[fact_name] = action['value']

                        if new_facts_found == False: 
                            break
                        
                        break 
        
        print("--- [IE] Inference completed. ---")
        ket_luan = known_facts.get("KET_LUAN")
        giai_thich = known_facts.get("GIAI_THICH")

        return ket_luan, giai_thich, solution_trace