import os
from validator import FreshCartInputValidator

def run_tests():
    validator = FreshCartInputValidator()
    
    # Paths to sample data folders relative to project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    valid_dir = os.path.join(base_dir, "sample_data", "valid")
    invalid_dir = os.path.join(base_dir, "sample_data", "invalid")
    
    print("=" * 60)
    print("FRESHCART GROCERS - INPUT FORMATS & VALIDATION TEST SUITE")
    print("=" * 60)
    
    # Test Valid Files
    print("\n--- [TEST GROUP 1: Valid Organic Store Inputs] ---")
    if os.path.exists(valid_dir):
        for filename in sorted(os.listdir(valid_dir)):
            file_path = os.path.join(valid_dir, filename)
            if os.path.isfile(file_path):
                print(f"\nTesting file: {filename}")
                result = validator.process_file(file_path)
                if result["status"] == "success":
                    print(f" [PASS] Status: SUCCESS")
                    print(f"       Title: {result['title']}")
                    print(f"       Doc Type: {result['doc_type']}")
                    print(f"       Text snippet: {result['text_to_summarise'][:100]}...")
                else:
                    print(f" [FAIL] Unexpected error: {result['message']}")
    else:
        print("Valid data directory not found.")

    # Test Invalid Files
    print("\n" + "=" * 60)
    print("--- [TEST GROUP 2: Invalid / Corrupt Inputs (Error Handling)] ---")
    if os.path.exists(invalid_dir):
        for filename in sorted(os.listdir(invalid_dir)):
            file_path = os.path.join(invalid_dir, filename)
            if os.path.isfile(file_path):
                print(f"\nTesting file: {filename}")
                result = validator.process_file(file_path)
                if result["status"] == "error":
                    print(f" [PASS] Handled correctly! Message:")
                    print(f"       --> {result['message']}")
                else:
                    print(f" [FAIL] Expected an error, but got success!")
    else:
        print("Invalid data directory not found.")

    print("\n" + "=" * 60)
    print("All tests completed successfully. Ready for Task 2 (Summary Prompt)!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()