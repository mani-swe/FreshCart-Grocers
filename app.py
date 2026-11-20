import os
import sys
import uuid
from flask import Flask, render_template, request, jsonify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.validator import FreshCartInputValidator
from src.summariser import FreshCartSummariser
from src.checklist_validator import FreshCartQualityValidator
from src.batch_processor import FreshCartBatchProcessor

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "temp_uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CHECKLIST_PATH = os.path.join(BASE_DIR, "config", "quality_checklist.json")
if not os.path.exists(CHECKLIST_PATH):
    CHECKLIST_PATH = os.path.join(BASE_DIR, "handover", "config", "quality_checklist.json")

input_validator = FreshCartInputValidator()
summariser = FreshCartSummariser()
qc_validator = FreshCartQualityValidator(CHECKLIST_PATH)
batch_processor = FreshCartBatchProcessor()

MODE_CONFIG = {
    "validator": {
        "label": "Input Validator",
        "eligible_formats": [".txt", ".md", ".json", ".csv"],
        "hint": "Validates whether a meeting transcript, store report (.json), or inventory log (.csv) is ready for summariser prompt generation."
    },
    "summariser": {
        "label": "Summary Prompt Generator",
        "eligible_formats": [".txt", ".md", ".json", ".csv"],
        "hint": "Validates the input file and generates the FreshCart system persona and structured summary prompt."
    },
    "qc_checklist": {
        "label": "Quality Control Checklist",
        "eligible_formats": [".json"],
        "hint": "Evaluates a produce delivery inspection JSON record against FreshCart quality checklist rules (QC_01 to QC_05)."
    },
    "batch_processing": {
        "label": "Batch Processing",
        "eligible_formats": [".json"],
        "hint": "Processes a JSON array of FreshCart orders and meeting notes while isolating broken rows and skipping duplicate IDs."
    }
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process_upload():
    mode = request.form.get("mode", "validator").strip()
    if mode not in MODE_CONFIG:
        return jsonify({
            "status": "error",
            "message": f"Error: Unknown operation mode '{mode}'."
        }), 400

    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "Error: No file part found in the upload request."
        }), 400

    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({
            "status": "error",
            "message": "Error: Please select a file before submitting."
        }), 400

    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()
    allowed_exts = MODE_CONFIG[mode]["eligible_formats"]

    if ext not in allowed_exts:
        return jsonify({
            "status": "error",
            "message": (
                f"Error: File format '{ext or 'none'}' is not eligible for "
                f"{MODE_CONFIG[mode]['label']}. Allowed formats: {', '.join(allowed_exts)}."
            )
        })

    safe_temp_name = f"{uuid.uuid4().hex}_{os.path.basename(file.filename)}"
    temp_path = os.path.join(UPLOAD_FOLDER, safe_temp_name)
    file.save(temp_path)

    try:
        if mode == "validator":
            res = input_validator.process_file(temp_path)
            if res.get("status") == "error":
                return jsonify(res)

            preview_len = len(res.get("text_to_summarise", ""))
            return jsonify({
                "status": "success",
                "mode": mode,
                "headline": "File is Valid & Ready for Summariser Prompt",
                "details": {
                    "source_file": res.get("source_file"),
                    "doc_type": res.get("doc_type"),
                    "title": res.get("title"),
                    "validated_text_length_chars": preview_len,
                    "summariser_readiness": "Eligible — can generate summariser prompt safely."
                },
                "preview_text": res.get("text_to_summarise", "")
            })

        if mode == "summariser":
            res = summariser.generate_summary(temp_path)
            if res.get("status") == "error":
                return jsonify(res)

            return jsonify({
                "status": "success",
                "mode": mode,
                "headline": "Summary Prompt Generated Successfully",
                "details": {
                    "source_file": res.get("source_file"),
                    "system_prompt": res.get("system_prompt")
                },
                "prompt_text": res.get("generated_user_prompt", "")
            })

        if mode == "qc_checklist":
            res = qc_validator.evaluate_inspection(temp_path)
            if res.get("status") == "error":
                return jsonify(res)

            return jsonify({
                "status": "success",
                "mode": mode,
                "headline": f"Quality Decision: {res.get('overall_decision')}",
                "details": {
                    "delivery_id": res.get("delivery_id"),
                    "produce_item": res.get("produce_item"),
                    "supplier_name": res.get("supplier_name"),
                    "overall_decision": res.get("overall_decision"),
                    "passed_count": res.get("passed_count"),
                    "failed_count": res.get("failed_count")
                },
                "checks": res.get("results", [])
            })

        if mode == "batch_processing":
            res = batch_processor.process_batch_file(temp_path)
            if res.get("status") == "error":
                return jsonify(res)

            return jsonify({
                "status": "success",
                "mode": mode,
                "headline": "Batch Processing Completed",
                "details": {
                    "source_file": res.get("source_file"),
                    "total_records": res.get("total_records"),
                    "processed_count": res.get("processed_count"),
                    "failed_count": res.get("failed_count"),
                    "skipped_duplicate_count": res.get("skipped_duplicate_count")
                },
                "processed_items": res.get("processed_items", []),
                "failed_items": res.get("failed_items", []),
                "skipped_duplicates": res.get("skipped_duplicates", [])
            })

    except Exception as exc:
        return jsonify({
            "status": "error",
            "message": f"Error: Unexpected server issue while processing file ({str(exc)})."
        })
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    app.run(debug=True, port=5000)