import json
import os
from .summariser import FreshCartSummariser


class FreshCartBatchProcessor:
    """
    Processes batches of FreshCart Grocers produce orders and meeting notes
    safely: isolates broken rows, prevents duplicate processing, and never crashes
    on malformed or empty inputs.
    """

    ALLOWED_RECORD_TYPES = {"produce_order", "meeting_note"}

    def __init__(self):
        self.summariser = FreshCartSummariser()

    def process_batch_file(self, batch_file_path: str) -> dict:
        if not os.path.exists(batch_file_path):
            return {
                "status": "error",
                "message": f"Error: Batch file not found at '{batch_file_path}'."
            }

        _, ext = os.path.splitext(batch_file_path)
        if ext.lower() != ".json":
            return {
                "status": "error",
                "message": f"Error: Unsupported batch format '{ext}'. Expected a '.json' array file."
            }

        try:
            with open(batch_file_path, "r", encoding="utf-8") as f:
                raw_text = f.read().strip()

            if not raw_text:
                return {
                    "status": "error",
                    "message": f"Error: Batch file '{os.path.basename(batch_file_path)}' is empty."
                }

            records = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            return {
                "status": "error",
                "message": f"Error: Invalid JSON in '{os.path.basename(batch_file_path)}' (line {exc.lineno}): {exc.msg}."
            }
        except Exception as exc:
            return {
                "status": "error",
                "message": f"Error: Could not read batch file ({str(exc)})."
            }

        if not isinstance(records, list) or len(records) == 0:
            return {
                "status": "error",
                "message": "Error: Batch JSON must contain a non-empty list of records."
            }

        seen_ids = set()
        processed_items = []
        failed_items = []
        skipped_duplicates = []

        for index, record in enumerate(records, start=1):
            item_result = self._process_single_record(record, index, seen_ids)
            status = item_result["status"]

            if status == "processed":
                processed_items.append(item_result)
            elif status == "skipped_duplicate":
                skipped_duplicates.append(item_result)
            else:
                failed_items.append(item_result)

        return {
            "status": "success",
            "source_file": os.path.basename(batch_file_path),
            "total_records": len(records),
            "processed_count": len(processed_items),
            "failed_count": len(failed_items),
            "skipped_duplicate_count": len(skipped_duplicates),
            "processed_items": processed_items,
            "failed_items": failed_items,
            "skipped_duplicates": skipped_duplicates
        }

    def _process_single_record(self, record, index: int, seen_ids: set) -> dict:
        if not isinstance(record, dict):
            return {
                "batch_item_id": f"ROW-{index}",
                "status": "failed",
                "error": f"Row {index} is not a valid JSON object."
            }

        item_id = str(record.get("batch_item_id") or f"ROW-{index}").strip()

        if item_id in seen_ids:
            return {
                "batch_item_id": item_id,
                "status": "skipped_duplicate",
                "reason": f"Duplicate batch_item_id '{item_id}' skipped to avoid redundant processing."
            }

        record_type = str(record.get("record_type", "")).strip()
        if record_type not in self.ALLOWED_RECORD_TYPES:
            return {
                "batch_item_id": item_id,
                "status": "failed",
                "error": f"Invalid or missing record_type '{record_type}'. Expected one of: {', '.join(sorted(self.ALLOWED_RECORD_TYPES))}."
            }

        supplier = str(record.get("supplier_or_source", "")).strip()
        item_or_topic = str(record.get("item_or_topic", "")).strip()
        unit = str(record.get("unit", "")).strip()
        delivery_day = str(record.get("delivery_day", "")).strip()
        notes = str(record.get("notes", "")).strip()
        quantity = record.get("quantity")

        if not item_or_topic or not supplier:
            return {
                "batch_item_id": item_id,
                "status": "failed",
                "error": "Missing required 'item_or_topic' or 'supplier_or_source'."
            }

        if isinstance(quantity, bool) or not isinstance(quantity, (int, float)) or quantity <= 0:
            return {
                "batch_item_id": item_id,
                "status": "failed",
                "error": f"Invalid quantity '{quantity}' for '{item_or_topic}': quantity must be a positive number."
            }

        if not unit or not delivery_day:
            return {
                "batch_item_id": item_id,
                "status": "failed",
                "error": f"Missing 'unit' or 'delivery_day' for '{item_or_topic}'."
            }

        seen_ids.add(item_id)

        raw_text = (
            f"Record ID: {item_id}\n"
            f"Type: {record_type}\n"
            f"Supplier / Source: {supplier}\n"
            f"Item / Topic: {item_or_topic}\n"
            f"Quantity: {quantity} {unit}\n"
            f"Delivery Day: {delivery_day}\n"
            f"Notes: {notes or 'None'}"
        )

        prompt_ready = self.summariser.build_user_prompt(
            title=f"{item_id} - {item_or_topic}",
            doc_type=record_type,
            raw_text=raw_text
        )

        return {
            "batch_item_id": item_id,
            "status": "processed",
            "record_type": record_type,
            "summary_line": f"{item_or_topic} ({quantity} {unit}) — {supplier} [{delivery_day}]",
            "prompt_length_chars": len(prompt_ready)
        }