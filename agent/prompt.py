import re


def detect_input_type(user_input: str) -> str:
    value = user_input.strip().lower()

    if re.match(r"^https?://", value):
        return "url"

    if value.startswith("how to"):
        return "howto"

    if re.search(r"\b(company|inc|corp|corporation|ltd|llc|plc)\b", value):
        return "company"

    if len(value.split()) <= 3:
        return "topic"

    return "general"


def build_system_instruction(user_input: str, profile: str = "auto", language: str = "English") -> str:
    detected_profile = detect_input_type(user_input) if profile == "auto" else profile

    base_rules = """
You are a senior web research analyst.

Rules:
- Research the user input thoroughly using web search and scraping when appropriate.
- Do not include hidden reasoning or chain-of-thought.
- Write only the final answer in clean markdown.
- Use evidence, summarize key points, and mention risks or uncertainties.
- If the input is a URL, analyze the page content.
- If the input is a company, produce an investment-style memo.
- If the input is a topic or general text, produce a concise research brief.
- CRITICAL: Write the entire report (including all headers and content) in {language}.
""".strip().format(language=language)

    company_output = """
Output format:

# Investment Memo: [Target]
**Date of Research:** [Current Date]

## 1. Overview
## 2. Key Findings
## 3. Risks / Caveats
## 4. Final Recommendation
""".strip()

    url_output = """
Output format:

# Web Page Analysis: [Target]
**Date of Research:** [Current Date]

## 1. Page Summary
## 2. Key Claims / Content
## 3. Trustworthiness / Risks
## 4. Final Takeaway
""".strip()

    topic_output = """
Output format:

# Research Brief: [Target]
**Date of Research:** [Current Date]

## 1. Topic Overview
## 2. Important Points
## 3. Contrasting Views / Risks
## 4. Final Takeaway
""".strip()

    general_output = """
Output format:

# Research Summary: [Target]
**Date of Research:** [Current Date]

## 1. What It Is
## 2. Key Information
## 3. Risks / Caveats
## 4. Final Takeaway
""".strip()

    howto_output = """
Output format:

# How-To Guide: [Target]
**Date of Research:** [Current Date]

## 1. Goal
## 2. Materials / Prerequisites
## 3. Step-by-Step Instructions
## 4. Tips / Risks / Safety Notes
## 5. Final Takeaway
""".strip()

    if detected_profile == "company":
        output = company_output
    elif detected_profile == "url":
        output = url_output
    elif detected_profile == "howto":
        output = howto_output
    elif detected_profile == "topic":
        output = topic_output
    else:
        output = general_output

    return f"{base_rules}\n\n{output}"


def build_prompt(user_input: str, profile: str = "auto", language: str = "English"):
    return build_system_instruction(user_input, profile, language)
