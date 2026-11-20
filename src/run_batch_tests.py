import os
from batch_processor import FreshCartBatchProcessor


def main():
    processor = FreshCartBatchProcessor()
    batch_dir = os.path.join("sample_data", "batch_samples")

    print("=" * 65)
    print("FRESHCART GROCERS - TASK 4: BATCH PROCESSING TEST RUNNER")
    print("=" * 65)

    for filename in sorted(os.listdir(batch_dir)):
        file_path = os.path.join(batch_dir, filename)
        if not os.path.isfile(file_path):
            continue

        print(f"\nBatch File: {filename}")
        res = processor.process_batch_file(file_path)

        if res["status"] == "error":
            print(f"  [HANDLED FILE ERROR] {res['message']}")
            continue

        print(
            f"  Total: {res['total_records']} | "
            f"Processed: {res['processed_count']} | "
            f"Failed: {res['failed_count']} | "
            f"Duplicates Skipped: {res['skipped_duplicate_count']}"
        )

        for item in res["processed_items"]:
            print(f"    [PROCESSED] {item['batch_item_id']}: {item['summary_line']}")

        for item in res["failed_items"]:
            print(f"    [FAILED ROW] {item['batch_item_id']}: {item['error']}")

        for item in res["skipped_duplicates"]:
            print(f"    [SKIPPED] {item['batch_item_id']}: {item['reason']}")


if __name__ == "__main__":
    main()