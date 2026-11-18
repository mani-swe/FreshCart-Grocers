import os
from .validator import FreshCartInputValidator

class FreshCartSummariser:
    """
    Handles prompt engineering and structured summarisation for FreshCart Grocers 
    meeting transcripts and store reports, building on top of input validation.
    """
    
    SYSTEM_PROMPT = (
        "You are an expert AI operations assistant for FreshCart Grocers, "
        "an organic grocery store chain. Your job is to analyze messy meeting transcripts "
        "or store reports and return a clean, structured executive summary focusing on: "
        "1. Executive Overview\n"
        "2. Key Decisions & Action Items (with owners and deadlines)\n"
        "3. Inventory & Stock Alerts (spoilage risks, low stock, reorders)\n"
        "4. Financial & Numerical Highlights (sales, losses, credits)"
    )

    def __init__(self):
        self.validator = FreshCartInputValidator()

    def build_user_prompt(self, title: str, doc_type: str, raw_text: str) -> str:
        """
        Constructs the structured prompt template to send to the LLM.
        """
        prompt = f"""
                Please analyze the following FreshCart Grocers document and generate a structured summary.

                Document Title: {title}
                Document Type: {doc_type}

                Content to Summarize:
                ---
                {raw_text}
                ---

                Provide the summary using the following exact headings:
                - **Executive Overview**
                - **Action Items & Owners**
                - **Inventory & Stock Alerts**
                - **Financial Highlights**
                """
        return prompt.strip()

    def generate_summary(self, file_path: str) -> dict:
        """
        Validates the file first, then generates the prompt-ready structure.
        (Integrates Task 1 validation with Task 2 prompt engineering).
        """
        # Step 1: Validate input using Task 1 logic
        validation_result = self.validator.process_file(file_path)
        
        if validation_result["status"] == "error":
            return validation_result  # Returns the clean error message without crashing

        # Step 2: Extract validated data
        title = validation_result["title"]
        doc_type = validation_result["doc_type"]
        text_to_summarise = validation_result["text_to_summarise"]

        # Step 3: Build prompt
        user_prompt = self.build_user_prompt(title, doc_type, text_to_summarise)

        # Note: In a live LLM integration, you would pass `SYSTEM_PROMPT` and `user_prompt` 
        # to your LLM API client here. For Task 2 delivery and testing, we structure and return 
        # the prompt package and a simulated structured summary format.
        
        return {
            "status": "success",
            "source_file": validation_result["source_file"],
            "system_prompt": self.SYSTEM_PROMPT,
            "generated_user_prompt": user_prompt,
            "simulated_structured_summary": f"""
            [AI SUMMARY GENERATED FOR: {title}]
            - Executive Overview: Successfully processed organic store document.
            - Action Items: Extracted from meeting/report data.
            - Inventory Status: Monitored for FreshCart inventory standards.
            """
        }