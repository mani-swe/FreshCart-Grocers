import json
import os


class FreshCartQualityValidator:
    """
    Loads FreshCart Grocers quality checklist rules from data (JSON)
    and evaluates staff inspection records without crashing on bad inputs.
    """

    def __init__(self, checklist_path: str = "config/quality_checklist.json"):
        self.checklist_path = checklist_path
        self.checklist_data = self._load_checklist(checklist_path)

    def _load_checklist(self, path: str) -> dict:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Checklist config file not found at '{path}'.")

        with open(path, "r", encoding="utf-8") as f:
            raw = f.read().strip()

        if not raw:
            raise ValueError(f"Checklist config file '{path}' is empty.")

        data = json.loads(raw)
        if "checks" not in data or not isinstance(data["checks"], list) or len(data["checks"]) == 0:
            raise ValueError(f"Checklist config '{path}' must contain a non-empty 'checks' list.")

        return data

    def evaluate_inspection(self, inspection_file_path: str) -> dict:
        """
        Validates an inspection record file against the loaded checklist rules.
        Returns a structured result dict or a clear human-readable error message.
        """
        if not os.path.exists(inspection_file_path):
            return {
                "status": "error",
                "message": f"Error: Inspection file not found at '{inspection_file_path}'."
            }

        _, ext = os.path.splitext(inspection_file_path)
        if ext.lower() != ".json":
            return {
                "status": "error",
                "message": f"Error: Unsupported inspection format '{ext}'. Expected a '.json' file."
            }

        try:
            with open(inspection_file_path, "r", encoding="utf-8") as f:
                raw_content = f.read().strip()

            if not raw_content:
                return {
                    "status": "error",
                    "message": f"Error: Inspection file '{os.path.basename(inspection_file_path)}' is empty."
                }

            record = json.loads(raw_content)
        except json.JSONDecodeError as exc:
            return {
                "status": "error",
                "message": f"Error: Invalid JSON in '{os.path.basename(inspection_file_path)}' (line {exc.lineno}): {exc.msg}."
            }
        except Exception as exc:
            return {
                "status": "error",
                "message": f"Error: Could not read '{os.path.basename(inspection_file_path)}' ({str(exc)})."
            }

        if not isinstance(record, dict):
            return {
                "status": "error",
                "message": "Error: Inspection record must be a JSON object."
            }

        responses = record.get("responses")
        if not isinstance(responses, dict) or not responses:
            return {
                "status": "error",
                "message": "Error: Missing or empty 'responses' object in inspection record."
            }

        checks = self.checklist_data.get("checks", [])
        check_results = []
        failed_checks = []
        has_critical_or_high_fail = False

        for check in checks:
            check_id = check["id"]
            check_name = check["name"]
            severity = check.get("severity", "medium")
            input_type = check.get("input_type")

            if check_id not in responses:
                return {
                    "status": "error",
                    "message": f"Error: Missing required checklist answer for '{check_id}' ({check_name})."
                }

            value = responses[check_id]
            eval_out = self._evaluate_single_check(check, input_type, value)

            if eval_out["status"] == "error":
                return eval_out

            passed = eval_out["passed"]
            check_results.append({
                "check_id": check_id,
                "name": check_name,
                "severity": severity,
                "passed": passed,
                "observed_value": value,
                "action": "Pass - acceptable per checklist rule." if passed else check.get("on_fail", "Review with supervisor.")
            })

            if not passed:
                failed_checks.append(check_id)
                if severity in {"critical", "high"}:
                    has_critical_or_high_fail = True

        if not failed_checks:
            overall_decision = "ACCEPT_DELIVERY"
        elif has_critical_or_high_fail:
            overall_decision = "HOLD_OR_REJECT_BATCH"
        else:
            overall_decision = "REVIEW_OR_DISCOUNT"

        return {
            "status": "success",
            "delivery_id": record.get("delivery_id", "UNKNOWN_DELIVERY"),
            "produce_item": record.get("produce_item", "Organic Produce"),
            "supplier_name": record.get("supplier_name", "Unknown Supplier"),
            "overall_decision": overall_decision,
            "passed_count": len(check_results) - len(failed_checks),
            "failed_count": len(failed_checks),
            "failed_checks": failed_checks,
            "results": check_results
        }

    def _evaluate_single_check(self, check: dict, input_type: str, value) -> dict:
        if input_type == "enum":
            allowed = check.get("allowed_values", [])
            passed_vals = check.get("pass_values", [])
            if not isinstance(value, str) or value not in allowed:
                return {
                    "status": "error",
                    "message": f"Error: Invalid value '{value}' for {check['id']}. Allowed values: {', '.join(allowed)}."
                }
            return {"status": "success", "passed": value in passed_vals}

        if input_type == "number_range_f":
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return {
                    "status": "error",
                    "message": f"Error: Temperature value for {check['id']} must be a number (°F), got '{value}'."
                }
            min_f = check.get("min_temp_f", 34.0)
            max_f = check.get("max_temp_f", 38.0)
            return {"status": "success", "passed": min_f <= float(value) <= max_f}

        if input_type == "min_days":
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return {
                    "status": "error",
                    "message": f"Error: Remaining shelf-life days for {check['id']} must be a number, got '{value}'."
                }
            min_days = check.get("min_remaining_days", 3)
            return {"status": "success", "passed": float(value) >= min_days}

        if input_type == "boolean":
            if not isinstance(value, bool):
                return {
                    "status": "error",
                    "message": f"Error: Value for {check['id']} must be true or false, got '{value}'."
                }
            required = check.get("required_value", True)
            return {"status": "success", "passed": value is required}

        if input_type == "tolerance_pct":
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return {
                    "status": "error",
                    "message": f"Error: Variance percentage for {check['id']} must be a number, got '{value}'."
                }
            max_var = abs(float(check.get("max_variance_pct", 5.0)))
            return {"status": "success", "passed": abs(float(value)) <= max_var}

        return {
            "status": "error",
            "message": f"Error: Unknown check input_type '{input_type}' configured for {check['id']}."
        }