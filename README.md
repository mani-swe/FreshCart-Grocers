# FreshCart Grocers - Meeting & Report Summariser (Task 1: Input Formats)

Welcome to the **FreshCart Grocers** AI project repository. FreshCart is a thriving organic grocery store chain committed to sustainable produce, zero food waste, and efficient store operations. To streamline daily management, this project builds an automated meeting and report summariser step-by-step—taking raw transcripts, daily logs, and store reports and turning them into concise, actionable summaries.

---

# 🚀 How to Run & Check

Make sure you have Python 3.x installed on your system.

   1. Open your terminal or command prompt in the project root folder.
   
   2. Run the test suite script:

```Bash
python src/main.py
```
   3. **What to expect:**

    - The script will automatically scan the sample_data/valid/ folder and successfully process meeting notes, store reports, and inventory CSV logs.

    - It will then scan the sample_data/invalid/ folder and gracefully catch empty files, short texts, and malformed JSONs, outputting clean, human-readable error messages without crashing.

---

## 📁 Repository Structure

```FreshCart-Grocers
.
├── src/
│   ├── __init__.py
│   ├── validator.py        # Input validation & standardization logic
│   └── main.py             # Test suite script
├── sample_data/
│   ├── valid/              # Realistic organic store sample files
│   │   ├── weekly_stock_meeting.txt
│   │   ├── daily_store_report.json
│   │   └── spoilage_log.csv
│   └── invalid/            # Intentional test files for error handling
│       ├── empty_file.txt
│       ├── missing_fields.json
│       └── too_short.txt
└── README.md               # Project documentation
└── .gitignore              # Git ignore rules
```