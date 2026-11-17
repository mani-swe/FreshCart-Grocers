import os
import json
import csv

class FreshCartInputValidator:
    """
    Validates and standardizes input documents (meetings, reports, logs) 
    for FreshCart Grocers before they are passed to the AI summariser.
    """
    
    ALLOWED_EXTENSIONS = {'.txt', '.md', '.json', '.csv'}
    MIN_CHAR_LENGTH = 50

    def process_file(self, file_path: str) -> dict:
        """
        Main entry point: checks if file exists, validates format and content,
        and returns a standardized dictionary or a clear error message.
        """
        # 1. Check if file exists
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"Error: File not found at '{file_path}'. Please check the path and try again."
            }

        # 2. Check file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            return {
                "status": "error",
                "message": f"Error: Unsupported format '{ext}'. FreshCart accepts: {', '.join(self.ALLOWED_EXTENSIONS)}."
            }

        # 3. Read file content based on extension
        try:
            if ext in {'.txt', '.md'}:
                return self._validate_text_file(file_path)
            elif ext == '.json':
                return self._validate_json_file(file_path)
            elif ext == '.csv':
                return self._validate_csv_file(file_path)
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error: Failed to parse file due to an unexpected format issue ({str(e)})."
            }

    def _validate_text_file(self, file_path: str) -> dict:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        # Check if empty
        if not content:
            return {
                "status": "error",
                "message": f"Error: The file '{os.path.basename(file_path)}' is empty. Nothing to summarise."
            }

        # Check minimum length requirement
        if len(content) < self.MIN_CHAR_LENGTH:
            return {
                "status": "error",
                "message": f"Error: Input content is too short ({len(content)} characters). Minimum {self.MIN_CHAR_LENGTH} characters required for a meaningful summary."
            }

        return {
            "status": "success",
            "source_file": os.path.basename(file_path),
            "doc_type": "meeting_transcript",
            "title": f"Meeting Notes: {os.path.basename(file_path)}",
            "text_to_summarise": content
        }

    def _validate_json_file(self, file_path: str) -> dict:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_text = f.read().strip()

        if not raw_text:
            return {
                "status": "error",
                "message": f"Error: The JSON file '{os.path.basename(file_path)}' is empty."
            }

        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError as jde:
            return {
                "status": "error",
                "message": f"Error: Invalid JSON syntax in '{os.path.basename(file_path)}' (Line {jde.lineno}): {jde.msg}"
            }

        # Validate required keys for store reports
        required_keys = ['title', 'content', 'date']
        missing_keys = [key for key in required_keys if key not in data]
        
        if missing_keys:
            return {
                "status": "error",
                "message": f"Error: Invalid report structure in '{os.path.basename(file_path)}'. Missing required field(s): {', '.join(missing_keys)}."
            }

        if not data['content'].strip():
            return {
                "status": "error",
                "message": f"Error: The 'content' field in '{os.path.basename(file_path)}' is empty."
            }

        return {
            "status": "success",
            "source_file": os.path.basename(file_path),
            "doc_type": data.get("doc_type", "store_report"),
            "title": data.get("title"),
            "text_to_summarise": f"Title: {data.get('title')}\nDate: {data.get('date')}\nBranch: {data.get('branch', 'Main Store')}\n\nContent:\n{data.get('content')}"
        }

    def _validate_csv_file(self, file_path: str) -> dict:
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            reader = list(csv.reader(f))

        if not reader:
            return {
                "status": "error",
                "message": f"Error: The CSV file '{os.path.basename(file_path)}' is empty."
            }

        headers = reader[0]
        rows = reader[1:]

        if not rows:
            return {
                "status": "error",
                "message": f"Error: CSV report '{os.path.basename(file_path)}' contains headers but no data rows."
            }

        # Format CSV rows into readable text for the summariser
        formatted_lines = [f"CSV Report Headers: {', '.join(headers)}", "Data Records:"]
        for row in rows:
            formatted_lines.append(" - " + ", ".join([f"{h}: {v}" for h, v in zip(headers, row)]))

        return {
            "status": "success",
            "source_file": os.path.basename(file_path),
            "doc_type": "inventory_log",
            "title": f"Inventory Log: {os.path.basename(file_path)}",
            "text_to_summarise": "\n".join(formatted_lines)
        }