# 🥬 FreshCart Grocers - Meeting & Report Summariser

Welcome to the **FreshCart Grocers** AI project repository. FreshCart is a thriving organic grocery store chain committed to sustainable produce, zero food waste, and efficient store operations. To streamline daily management, this project builds an automated meeting and report summariser step-by-step—taking raw transcripts, daily logs, and store reports and turning them into concise, actionable summaries.

---

## 🚀 How to Run & Check

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

---

## ✅ Quality Check Rules (Organic Produce Deliveries)

Quality rules are kept in `config/quality_checklist.json` rather than hardcoded in Python, and `FreshCartQualityValidator` (`src/checklist_validator.py`) checks each staff inspection record against those rules before a batch moves forward.

   ### Inspection Criteria (`QC_01` – `QC_05`)

   1. **QC_01_CONDITION (enum — High Severity — Produce Visual & Texture Condition)**

      - **Pass Rule:** Value is `fresh_firm` or `minor_wear` with no mold, rot, or heavy bruising so spoilage does not spread   to nearby stock.
      - **On Fail:** Quarantine affected crates, log spoilage, and raise supplier credit or rejection for widespread damage.

   2. **QC_02_COLD_CHAIN (number_range_f — Critical Severity — Cold Chain Storage Temperature)**

      - **Pass Rule:** Chilled produce is between `34.0°F` and `38.0°F` (`1.1°C` to `3.3°C`) to protect freshness and slow bacterial growth.
      - **On Fail:** Flag temperature breach, place batch on hold, and notify the store manager before storage or display.

   3. **QC_03_SHELF_LIFE (min_days — High Severity — Remaining Shelf-Life & Freshness Window)**

      - **Pass Rule:** At least `3` days of usable shelf life remain from delivery so customers get fresh organic items and waste stays low.
      - **On Fail:** Mark sound short-dated stock (`1–2` days) for fast-sale/discount, or reject/log waste if expired or spoiled.

   4. **QC_04_PACKAGING_LABEL (boolean — Critical Severity — Packaging Integrity & Organic Lot Labeling)**

      - **Pass Rule:** Crates and seals are intact (`true`) with no leaks/contamination and clear organic lot/origin traceability.
      - **On Fail:** Hold unlabelled or damaged-seal crates and request organic certification or lot verification from the supplier.

   5. **QC_05_QUANTITY_WEIGHT (tolerance_pct — Medium Severity — Delivered Quantity vs. Order Tolerance)**
      - **Pass Rule:** Actual weight or unit count variance stays within `±5.0%` of the approved purchase order.
      - **On Fail:** Record quantity variance on the receiving slip and log a short-delivery or over-delivery adjustment.

   ### Overall Batch Decision Logic & Error Safety

   - **ACCEPT_DELIVERY**: All 5 checks pass (`0` failed checks) and the delivery can be accepted into normal workflow.
   - **HOLD_OR_REJECT_BATCH**: One or more `critical` or `high` severity checks fail, requiring immediate hold, discount/     spoilage handling, or rejection.
   - **REVIEW_OR_DISCOUNT**: Non-critical checks fail and need store review or pricing adjustment.
   - **Error Handling**: Empty files, malformed JSON, missing `responses` or check answers, and invalid field types return clear error messages without crashing.

---

## ❓ What to Expect?:

Up to this stage (**Task 3: Quality Checklist**), the **FreshCart Grocers** project covers input validation, structured summary prompt preparation, and data-driven organic produce quality checks:

   - **Input Validation & Standardisation (`src/validator.py`):** Accepts `.txt`, `.md`, `.json`, and `.csv` store files with realistic organic grocery data (such as `weekly_stock_meeting.txt`, `daily_store_report.json`, and `spoilage_log.csv`), normalises valid content, and returns clear error messages instead of crashing on empty, short, missing-field, or unsupported files.

   - **Summary Prompt Preparation (`src/summariser.py`):** Builds on validated inputs to generate the FreshCart system persona and structured prompt instructions covering executive overview, action items with owners, inventory/spoilage alerts, and financial highlights.

   - **Quality Checklist Evaluation (`config/quality_checklist.json` & `src/checklist_validator.py`):** Evaluates organic produce inspection records across `QC_01_CONDITION`, `QC_02_COLD_CHAIN` (`34.0°F`–`38.0°F`), `QC_03_SHELF_LIFE`, `QC_04_PACKAGING_LABEL`, and `QC_05_QUANTITY_WEIGHT`, returning `ACCEPT_DELIVERY`, `HOLD_OR_REJECT_BATCH`, or `REVIEW_OR_DISCOUNT` along with failure actions and safe error messages on bad inputs.

   - **CLI Test Runners & Optional Web Interface (`src/main.py`, `src/run_qc_tests.py`, `app.py`):** Lets you verify all checks from the terminal or upload files through the Flask web interface (`templates/index.html`)

---

## 📁 Repository Structure

```FreshCart-Grocers
.
├── src/
│   ├── __init__.py
│   ├── checklist_validator.py         # Task 3: Quality checklist rule evaluator
│   ├── validator.py                   # Input validation & standardization logic
│   ├── summariser.py                  # Extraact useful information from file and generate clean prompt for AI model 
│   ├── run_qc_tests.py                # Task 3: Quality checklist test runner
│   └── main.py                        # Test suite script
├── sample_data/
│   ├── invalid/                       # Intentional test files for error handling
│   ├── qc_samples/                    # Organic produce inspection test records
│   └── valid/                         # Realistic organic store sample files
├── config/
│   └── quality_checklist.json         # Data-driven produce quality rules & fail actions
├── templates/
│   └── index.html                     # Simple web UI for uploading store files
├── app.py                             # Flask web interface for file upload & validation
├── README.md                          # Project documentation
├── requirements.txt                   # Project dependencies
└── .gitignore                         # Git ignore rules
```