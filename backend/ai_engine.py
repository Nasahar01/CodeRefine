import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise Exception("❌ GROQ_API_KEY not found")

client = Groq(api_key=api_key)

def analyze_code(code, language, mode):
    
    if mode == "review":
        prompt = f"""
You are an expert software engineer.

Analyze the {language} code below.

Rules:
- Write clear short points.
- Do NOT add explanations outside sections.
- Follow EXACT format.

BUGS:
(list bugs or say "No bugs found")

PERFORMANCE:
(list issues or say "No performance issues")

SECURITY:
(list risks or say "No security issues")

BEST_PRACTICES:
(list improvements)

OPTIMIZED_CODE:
(provide improved code only)

Code:
{code}
"""

    else:
        prompt = f"""
You are an expert software engineer.

Rewrite and optimize the following {language} code.
Return ONLY the improved code.
Do NOT include markdown, explanations, or backticks.

Code:
{code}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=900
    )

    output = response.choices[0].message.content.strip()

    # Remove ``` if model still returns it
    output = output.replace("```python", "").replace("```", "").strip()

    return output

