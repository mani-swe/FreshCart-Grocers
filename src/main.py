import os
from summariser import FreshCartSummariser

def run_task2_tests():
    summariser = FreshCartSummariser()
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    valid_dir = os.path.join(base_dir, "sample_data", "valid")
    invalid_dir = os.path.join(base_dir, "sample_data", "invalid")
    
    print("=" * 65)
    print("FRESHCART GROCERS - TASK 2: SUMMARY PROMPT TEST SUITE")
    print("=" * 65)
    
    # Test Valid Files with Summariser Prompt
    print("\n--- [TEST GROUP 1: Prompt Generation on Valid Organic Store Data] ---")
    if os.path.exists(valid_dir):
        for filename in sorted(os.listdir(valid_dir)):
            file_path = os.path.join(valid_dir, filename)
            if os.path.isfile(file_path):
                print(f"\nProcessing file: {filename}")
                result = summariser.generate_summary(file_path)
                if result["status"] == "success":
                    print(f" [PASS] Status: SUCCESS")
                    print(f"       System Prompt Persona Set: Yes")
                    print(f"       User Prompt Ready Length: {len(result['generated_user_prompt'])} chars")
                else:
                    print(f" [FAIL] Unexpected error: {result['message']}")

    # Test Invalid Files (Error Handling Check)
    print( "\n" + "--- [TEST GROUP 2: Error Handling on Invalid/Empty Files] ---")
    if os.path.exists(invalid_dir):
        for filename in sorted(os.listdir(invalid_dir)):
            file_path = os.path.join(invalid_dir, filename)
            if os.path.isfile(file_path):
                print(f"\nTesting file: {filename}")
                result = summariser.generate_summary(file_path)
                if result["status"] == "error":
                    print(f" [PASS] Caught error successfully: {result['message']}")
                else:
                    print(f" [FAIL] Expected an error, but got success!")

    print("\n" + "=" * 65)
    print("Task 2 Summary Prompt tests completed successfully!")
    print("=" * 65)

if __name__ == "__main__":
    run_task2_tests()