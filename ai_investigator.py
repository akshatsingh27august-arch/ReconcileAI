import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def investigate_exception(exception_data):

    prompt = f"""
You are ReconcileAI, an AI Finance Controller helping a finance
operations team investigate reconciliation exceptions.

Analyze ONLY the transaction evidence provided below.

IMPORTANT RULES:

1. Use ONLY the evidence provided.
2. Do not invent missing transaction details.
3. Clearly distinguish facts from inference.
4. Do not assume the external payment gateway or bank is at fault
   unless the evidence proves it.
5. If the exact root cause cannot be confirmed from the evidence,
   say so clearly.
6. Recommend a practical next investigation step.
7. Never approve, reject, refund, or make a final financial decision.
8. A human must make the final financial decision.

TRANSACTION EVIDENCE:

{exception_data}

Return your response using exactly these sections:

ROOT CAUSE:
State the most likely operational explanation.
Clearly label anything that is an inference.
If the exact cause cannot be confirmed from the evidence, say that.

EVIDENCE:
List the specific transaction facts supporting the conclusion.

RECOMMENDED ACTION:
Give the finance operations team the next practical investigation
or resolution step.

RISK LEVEL:
Choose exactly one: LOW, MEDIUM, or HIGH.

HUMAN REVIEW:
Choose exactly one: REQUIRED or NOT REQUIRED.

CONFIDENCE:
Choose exactly one: LOW, MEDIUM, or HIGH.

Do not invent transaction information.
Do not make financial decisions.
"""

    # Try the Gemini request up to 2 times.
    # A 503 error usually means temporary high demand.
    for attempt in range(2):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            # Retry only temporary Gemini server errors.
            if "503" in error_message and attempt == 0:

                time.sleep(3)
                continue

            raise e