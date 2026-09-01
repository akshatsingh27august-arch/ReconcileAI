import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=GEMINI_API_KEY)


def investigate_exception(exception_data):

    prompt = f"""
You are an AI Finance Controller investigating a transaction reconciliation exception.

Analyze ONLY the evidence provided below.

Transaction evidence:
{exception_data}

Return your response in exactly this structure:

ROOT CAUSE:
Explain the most likely reason for the exception.

EVIDENCE:
Mention the important transaction facts supporting your conclusion.

RECOMMENDED ACTION:
Give a practical action for the finance operations team.

RISK LEVEL:
Choose exactly one: LOW, MEDIUM, or HIGH.

HUMAN REVIEW:
Choose exactly one: REQUIRED or NOT REQUIRED.

Do not invent transaction information.
Do not make financial decisions or approve/reject payments.
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            if "503" in str(e) and attempt < 2:
                time.sleep(3)
                continue

            raise e