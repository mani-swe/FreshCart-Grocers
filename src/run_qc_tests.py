import os
from checklist_validator import FreshCartQualityValidator


def main():
    validator = FreshCartQualityValidator("config/quality_checklist.json")
    samples_dir = os.path.join("sample_data", "qc_samples")

    print("=" * 65)
    print("FRESHCART GROCERS - TASK 3: QUALITY CHECKLIST VALIDATION")
    print("=" * 65)

    for filename in sorted(os.listdir(samples_dir)):
        path = os.path.join(samples_dir, filename)
        if not os.path.isfile(path):
            continue

        print(f"\nFile: {filename}")
        res = validator.evaluate_inspection(path)

        if res["status"] == "success":
            print(f"  Delivery : {res['delivery_id']} | Item: {res['produce_item']}")
            print(f"  Decision : {res['overall_decision']} (Passed: {res['passed_count']}, Failed: {res['failed_count']})")
            for item in res["results"]:
                mark = "PASS" if item["passed"] else "FAIL"
                print(f"    [{mark}] {item['check_id']} -> {item['action']}")
        else:
            print(f"  [HANDLED ERROR] {res['message']}")


if __name__ == "__main__":
    main()