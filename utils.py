# services/utils.py
import time
from google.api_core.exceptions import ResourceExhausted

def safe_generate_content(model, prompt, retry_delay=40):
    try:
        return model.generate_content(prompt).text.strip()
    except ResourceExhausted as e:
        if "quota" in str(e).lower():
            print("⏳ Gemini quota exceeded. Retrying...")
            time.sleep(retry_delay)
            return model.generate_content(prompt).text.strip()
        raise e
