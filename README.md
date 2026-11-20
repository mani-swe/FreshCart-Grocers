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

## 📦 How Batch Processing Works & Validation Criteria

`FreshCartBatchProcessor` (`src/batch_processor.py`) reads a batch of FreshCart Grocers orders and meeting notes (such as `sample_data/batch_samples/freshcart_batch_orders.json`) and processes items one by one without stopping the batch when an individual row is bad or a file is empty.

   ### How It Runs

   1. **File-Level Safety Check:** Verifies that the batch file exists, uses `.json`, is not empty, parses as valid JSON, and contains a non-empty list of records. If not, it returns a clear error message without crashing.

   2. **Per-Record Validation & Isolation:** Each item in the list is checked separately. Bad rows are logged under `failed_items` with a clear reason while valid rows continue into `processed_items`.

   3. **Duplicate ID Protection:** Tracks `batch_item_id` values already seen in the run and marks repeats as `skipped_duplicate` so duplicate entries do not waste processing or model cost.

   4. **Batch Summary Output:** Returns total counts (`total_records`, `processed_count`, `failed_count`, `skipped_duplicate_count`) along with processed summaries, failure reasons, and skipped duplicates.

   ### Criteria Used to Validate Batch Items

   - **Record Structure & Type (`record_type`):** Each entry must be a JSON object with `record_type` set to `produce_order` or `meeting_note`.

   - **Supplier / Source & Item / Topic (`supplier_or_source`, `item_or_topic`):** Both fields must be non-empty text (for example, `GreenValley Organic Farms` and `Organic kale`).

   - **Positive Quantity (`quantity`):** Must be a valid number greater than `0` (not text, boolean, zero, or a negative value like `-5`).

   - **Unit & Delivery Timing (`unit`, `delivery_day`):** Both fields must be non-empty (for example, `12` `bunches` on `Thursday`).

   - **Unique Batch ID (`batch_item_id`):** Repeated IDs within the batch are skipped as duplicates instead of being re-processed.

---

## ❓ What to Expect?:

Up to this stage, the **FreshCart Grocers** project covers input validation, structured summary prompt building, organic produce quality checks, and safe batch record processing:

   - **Input Validation & Standardisation (`src/validator.py`):** Validates `.txt`, `.md`, `.json`, and `.csv` store files with realistic organic grocery sample data, normalises valid inputs, and returns clear error messages on empty, short, missing-field, or unsupported files without crashing.

   - **Summary Prompt Preparation (`src/summariser.py`):** Builds on validated inputs to generate the FreshCart system persona and structured prompt template covering executive overview, action items with owners, inventory/spoilage alerts, and financial highlights.

   - **Quality Checklist Evaluation (`config/quality_checklist.json` & `src/checklist_validator.py`):** Evaluates organic produce inspection records across `QC_01_CONDITION`, `QC_02_COLD_CHAIN` (`34.0°F`–`38.0°F`), `QC_03_SHELF_LIFE`, `QC_04_PACKAGING_LABEL`, and `QC_05_QUANTITY_WEIGHT`, returning `ACCEPT_DELIVERY`, `HOLD_OR_REJECT_BATCH`, or `REVIEW_OR_DISCOUNT` with failure actions and safe error handling.

   - **Batch Processing & Error Isolation (`src/batch_processor.py` & `src/run_batch_tests.py`):** Processes batches of grocery orders and meeting notes, isolates invalid rows (`BATCH-003` and `BATCH-004`) and empty batch files (`empty_batch.json`) with clear messages, and skips duplicate IDs.

---

## 📁 Repository Structure

```FreshCart-Grocers
.
├── src/
│   ├── __init__.py
│   ├── run_batch_tests.py             # Batch processing test runner
│   ├── checklist_validator.py         # Quality checklist rule evaluator
│   ├── validator.py                   # Input validation & standardization logic
│   ├── summariser.py                  # Extraact useful information from file and generate clean prompt for AI model
│   ├── batch_processor.py             # Safe batch record & duplicate processor
│   ├── run_qc_tests.py                # Quality checklist test runner
│   └── main.py                        # Test suite script
├── sample_data/
│   ├── batch_samples/                 # Batch order/meeting records & empty batch test
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