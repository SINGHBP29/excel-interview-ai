# evaluation_service.py
import json
from utils import safe_generate_content

def evaluate_answer(model, question, answer):
    prompt = f"""
You are a senior Excel expert evaluating a candidate’s response.

Evaluate the answer based on:
1. Accuracy
2. Clarity
3. Relevance

### Question:
{question}

### Candidate Answer:
{answer}

Respond strictly in JSON format:
{{
  "score": <0 to 5>,
  "feedback": "<brief feedback>"
}}
"""
    try:
        raw = safe_generate_content(model, prompt)

        # Try to extract JSON
        start = raw.find("{")
        end = raw.rfind("}")
        json_str = raw[start:end + 1]

        parsed = json.loads(json_str)
        return parsed["score"], parsed["feedback"]

    except Exception as e:
        return 0, f"⚠️ Evaluation failed: {str(e)}"
