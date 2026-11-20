import os
import sys

# Ensure handover directory is on sys.path so relative/package imports work
# whether run directly or via module execution.
HANDOVER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if HANDOVER_DIR not in sys.path:
    sys.path.insert(0, HANDOVER_DIR)

from validator import FreshCartInputValidator
from summariser import FreshCartSummariser
from checklist_validator import FreshCartQualityValidator
from batch_processor import FreshCartBatchProcessor


def run_handover_pipeline() -> None:
    checklist_path = os.path.join(HANDOVER_DIR, "config", "quality_checklist.json")
    sample_root = os.path.join(HANDOVER_DIR, "sample_data")

    input_validator = FreshCartInputValidator()
    summariser = FreshCartSummariser()
    qc_validator = FreshCartQualityValidator(checklist_path)
    batch_processor = FreshCartBatchProcessor()

    print("=" * 68)
    print("FRESHCART GROCERS - TASK 5: END-TO-END HANDOVER PIPELINE CHECK")
    print("=" * 68)

    # 1. Input Validation & Summary Prompt Generation (Valid Files)
    print("\n--- [1. Valid Store Inputs & Summary Prompt] ---")
    valid_dir = os.path.join(sample_root, "valid")
    if os.path.exists(valid_dir):
        for filename in sorted(os.listdir(valid_dir)):
            file_path = os.path.join(valid_dir, filename)
            if not os.path.isfile(file_path):
                continue

            val_res = input_validator.process_file(file_path)
            sum_res = summariser.generate_summary(file_path)

            if val_res["status"] == "success" and sum_res["status"] == "success":
                print(f"  [PASS] {filename} -> type={val_res['doc_type']}, prompt_chars={len(sum_res['generated_user_prompt'])}")
            else:
                print(f"  [FAIL] {filename} -> {val_res.get('message') or sum_res.get('message')}")
    else:
        print(f"  [WARN] Missing directory: {valid_dir}")

    # 2. Bad / Empty Input Safety Check
    print("\n--- [2. Invalid & Empty Input Error Handling] ---")
    invalid_dir = os.path.join(sample_root, "invalid")
    if os.path.exists(invalid_dir):
        for filename in sorted(os.listdir(invalid_dir)):
            file_path = os.path.join(invalid_dir, filename)
            if not os.path.isfile(file_path):
                continue

            res = summariser.generate_summary(file_path)
            if res["status"] == "error":
                print(f"  [HANDLED ERROR] {filename} -> {res['message']}")
            else:
                print(f"  [UNEXPECTED] {filename} -> {res['status']}")
    else:
        print(f"  [WARN] Missing directory: {invalid_dir}")

    # 3. Organic Produce Quality Checklist Evaluation
    print("\n--- [3. Organic Produce Quality Checklist] ---")
    qc_dir = os.path.join(sample_root, "qc_samples")
    if os.path.exists(qc_dir):
        for filename in sorted(os.listdir(qc_dir)):
            file_path = os.path.join(qc_dir, filename)
            if not os.path.isfile(file_path):
                continue

            qc_res = qc_validator.evaluate_inspection(file_path)
            if qc_res["status"] == "success":
                print(
                    f"  [PASS] {filename} -> {qc_res['produce_item']} "
                    f"({qc_res['delivery_id']}): {qc_res['overall_decision']}"
                )
            else:
                print(f"  [HANDLED ERROR] {filename} -> {qc_res['message']}")
    else:
        print(f"  [WARN] Missing directory: {qc_dir}")

    # 4. Batch Processing Check
    print("\n--- [4. Batch Processing Pipeline] ---")
    batch_dir = os.path.join(sample_root, "batch_samples")
    if os.path.exists(batch_dir):
        for filename in sorted(os.listdir(batch_dir)):
            file_path = os.path.join(batch_dir, filename)
            if not os.path.isfile(file_path):
                continue

            batch_res = batch_processor.process_batch_file(file_path)
            if batch_res["status"] == "success":
                print(
                    f"  [PASS] {filename} -> total={batch_res['total_records']}, "
                    f"processed={batch_res['processed_count']}, "
                    f"failed={batch_res['failed_count']}, "
                    f"skipped_duplicates={batch_res['skipped_duplicate_count']}"
                )
            else:
                print(f"  [HANDLED ERROR] {filename} -> {batch_res['message']}")
    else:
        print(f"  [WARN] Missing directory: {batch_dir}")

    print("\n" + "=" * 68)
    print("Handover end-to-end check finished without crashes.")
    print("=" * 68)


if __name__ == "__main__":
    run_handover_pipeline()