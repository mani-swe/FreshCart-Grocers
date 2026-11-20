# FreshCart Grocers — Meeting & Report Summariser

An operations and reporting assistant developed for **FreshCart Grocers** (an organic grocery store chain). The application validates store documents, generates structured LLM summarisation prompts, evaluates organic produce delivery quality inspections against data-driven rules (`QC_01`–`QC_05`), and processes batch inventory/order files safely through both a unified **Flask Web Hub** and an end-to-end **CLI Handover Pipeline**.

---

## 🚀 Features

- **Multi-Format Input Validator (`src/validator.py`):** Validates `.txt`, `.md`, `.json`, and `.csv` store files for supported extensions, non-empty content, minimum length thresholds, and required schema fields before summarisation.
- **Structured Summary Prompt Builder (`src/summariser.py`):** Wraps validated transcripts, daily store reports, and inventory logs into an expert FreshCart system persona and structured user prompt ready for LLM execution.
- **Data-Driven Quality Control Checklist (`src/checklist_validator.py`):** Evaluates organic produce delivery inspection records against configurable JSON rules (`QC_01` through `QC_05`) and returns clear operational decisions (`ACCEPT_DELIVERY`, `HOLD_OR_REJECT_BATCH`, or `REVIEW_OR_DISCOUNT`).
- **Fault-Tolerant Batch Processor (`src/batch_processor.py`):** Processes JSON arrays of store orders and meeting notes while isolating malformed rows (e.g., negative quantities or missing fields) and skipping duplicate batch IDs without crashing.
- **4-Mode Interactive Web Hub (`app.py` & `templates/index.html`):** Clean, responsive web interface allowing staff to select an operational mode, view eligible file formats, upload documents, and inspect tailored outputs in real time.
- **End-to-End CLI Handover Pipeline (`handover/src/run_handover.py`):** Single-command verification script running all four modules across valid, invalid, quality control, and batch test datasets.

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3 (Responsive Grid & Overflow-Safe Cards), Vanilla JavaScript (Fetch API)
- **Backend:** Python 3, Flask
- **Data & Rule Processing:** Python Standard Library (`json`, `csv`, `os`, `uuid`, `pathlib`)
- **Configuration & Sample Datasets:** JSON rule schemas (`config/quality_checklist.json`) & multi-format store fixtures (`sample_data/`)

---

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed on your system:

- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

---

## 📥 Installation & Setup Instructions

Follow these instructions and run these commands step-by-step in your VS Code terminal to get the project running locally:

### 1. Clone the Repository

```bash
git clone https://github.com/mani-swe/FreshCart-Grocers.git
cd FreshCart-Grocers
```

### 2. Setup a Virtual Environment

- **On Windows:**
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

- **On macOS/Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📚 Core Pipeline Modules & Supported Formats

The application routes store files through four specialized modules depending on the selected operation:

### 1. Input Validator & Summary Prompt (`src/validator.py`, `src/summariser.py`)

- **Eligible Formats:** `.txt`, `.md`, `.json`, `.csv`
- **Validation Rules:**
  - Rejects empty files or unsupported extensions with clear error messages.
  - Enforces a minimum of 50 characters on plain-text meeting transcripts (`.txt`, `.md`).
  - Verifies required structured keys in daily store reports (`.json`) and non-empty rows in inventory/spoilage logs (`.csv`).
- **Prompt Assembly:** Produces a domain-tuned FreshCart system prompt alongside a structured user prompt highlighting key updates, stock alerts, and action items.

### 2. Organic Produce Quality Checklist (`config/quality_checklist.json`, `src/checklist_validator.py`)

- **Eligible Format:** `.json`
- **Checklist Rules (`QC_01` – `QC_05`):**
  - `QC_01_CONDITION`: Produce Visual & Texture Condition
  - `QC_02_PACKAGING`: Packaging & Cold-Chain Integrity
  - `QC_03_ORGANIC_CERT`: Organic Certification & Lot Traceability
  - `QC_04_TEMPERATURE`: Delivery Transit Temperature Compliance
  - `QC_05_QUANTITY_WEIGHT`: Delivered Quantity & Weight Accuracy
- **Outcomes:** Computes pass/fail counts, per-rule corrective actions, and an overall batch decision (`ACCEPT_DELIVERY`, `HOLD_OR_REJECT_BATCH`, or `REVIEW_OR_DISCOUNT`).

### 3. Safe Batch Processing (`src/batch_processor.py`)

- **Eligible Format:** `.json` (array of order/meeting records)
- **Resilience Guarantees:**
  - Isolates broken records (missing fields, invalid types, negative quantities) into `failed_items` without halting the batch.
  - Detects and skips repeated `batch_item_id` entries into `skipped_duplicates`.

---

## 🚀 Launch the Application

### Option A: Start the Flask Web Hub (4-Mode UI)

1. Run the Flask server from the project root:
   ```bash
   python app.py
   ```
2. Open this link in your web browser:
   ```text
   http://127.0.0.1:5000/
   ```
3. Choose any of the **4 Operations** at the top (`Input Validator`, `Summary Prompt`, `Quality Control`, or `Batch Processing`), review the eligible file badges, upload a sample file from `sample_data/`, and inspect the output panel below.

### Option B: Run the End-to-End Handover Pipeline (CLI)

Execute the standalone handover verification script in your terminal:

```bash
python handover/src/run_handover.py
```

This runs all four pipeline stages sequentially against `handover/sample_data/` and prints pass/fail and error-handling diagnostics in the terminal.

---

## 📋 Handover Summary

- **What Was Built:** End-to-end input validator, structured LLM summary prompt builder, rule-driven organic produce quality checklist (`QC_01`–`QC_05`), fault-tolerant batch processor, standalone CLI handover runner (`handover/src/run_handover.py`), and a 4-mode Flask web application (`app.py` + `templates/index.html`).
- **Current Scope Boundaries:** External live LLM API execution and cloud database persistence are intentionally excluded from this handover milestone, which focuses on deterministic validation, prompt generation, rule evaluation, batch safety, and local/web verification.
- **Recommended Next Steps:** Connect the generated prompt payload in `FreshCartSummariser` to an LLM inference endpoint (e.g., Groq/OpenAI) and add persistent storage for daily QC and batch audit logs.

---

## 📁 Project Structure

```text
FreshCart-Grocers/
├── app.py                             # Main Flask web server & 4-mode upload router
├── README.md                          # Project documentation & handover guide
├── requirements.txt                   # Python dependencies (Flask, etc.)
├── temp_uploads/                      # Temporary staging folder for uploaded files
├── templates/   
│   └── index.html                     # 4-mode interactive web UI
├── config/  
│   └── quality_checklist.json         # Data-driven produce QC rules (QC_01–QC_05)
├── sample_data/   
│   ├── valid/                         # Valid store transcripts, JSON reports & CSV logs
│   ├── invalid/                       # Empty, short & malformed test inputs
│   ├── qc_samples/                    # Produce delivery inspection JSON fixtures
│   └── batch_samples/                 # Multi-record & empty batch JSON fixtures
├── src/   
│   ├── __init__.py
│   ├── run_batch_tests.py             # Batch processing test runner
│   ├── checklist_validator.py         # Quality checklist rule evaluator
│   ├── validator.py                   # Input validation & standardization logic
│   ├── summariser.py                  # Extraact useful information from file and generate clean prompt for AI model
│   ├── batch_processor.py             # Safe batch record & duplicate processor
│   └── run_qc_tests.py                # Quality checklist test runner
└── handover/
    ├── config/
    │   └── quality_checklist.json     # Handover copy of produce QC checklist rules
    ├── sample_data/                   # Self-contained test datasets for CLI handover check
    │   ├── valid/
    │   ├── invalid/
    │   ├── qc_samples/
    │   └── batch_samples/
    └── src/
        ├── __init__.py
        ├── validator.py
        ├── summariser.py
        ├── checklist_validator.py
        ├── batch_processor.py
        └── run_handover.py            # End-to-end CLI verification runner
```