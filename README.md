# FreshCart Grocers - Meeting & Report Summariser (Task 1: Input Formats)

Welcome to the **FreshCart Grocers** AI project repository. FreshCart is a thriving organic grocery store chain committed to sustainable produce, zero food waste, and efficient store operations. To streamline daily management, this project builds an automated meeting and report summariser step-by-step—taking raw transcripts, daily logs, and store reports and turning them into concise, actionable summaries.

---

# 🚀 How to Run & Check

Make sure you have Python 3.x installed on your system.

   - Open your terminal or command prompt in the project root folder.
   
   - Run the test suite script:

```Bash
python src/main.py
```

   - Or if you want to run flask application:

      1. Install dependencies in your terminal:

```Bash
pip install -r requirements.txt
``` 
      2. Now run flask application by:

```Bash
python app.py
``` 

      3. Now open this link in your browser: http://127.0.0.1:5000

   - **What to expect:**

      - The script validates all organic grocery store sample files (.txt, .json, .csv).

      - For valid files, it successfully sets the expert system persona and generates the structured LLM prompt ready for summarisation.

      - For invalid files, it gracefully catches empty files, missing JSON fields, and short texts, outputting clean, human-readable error messages without crashing.

---

## 📁 Repository Structure

```FreshCart-Grocers
.
├── src/
│   ├── __init__.py
│   ├── validator.py        # Input validation & standardization logic
│   ├── summariser.py       # Extraact useful information from file and generate clean prompt for AI model 
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
├── templates/
│   └── index.html          # Frontend user interface
├── app.py                  # Flask Application that gives GUI to project
├── README.md               # Project documentation
└── .gitignore              # Git ignore rules
```