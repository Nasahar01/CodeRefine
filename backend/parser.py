import re

def parse_review_response(text):
    sections = ["BUGS", "PERFORMANCE", "SECURITY", "BEST_PRACTICES", "OPTIMIZED_CODE"]
    result = {}

    for sec in sections:
        pattern = rf"{sec}:\s*(.*?)(?=\n[A-Z_]+:|$)"
        match = re.search(pattern, text, re.S | re.I)

        if match:
            result[sec] = match.group(1).strip()
        else:
            result[sec] = "No issues found."

    return result
