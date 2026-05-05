from agent.agent import create_agent
from html import escape
import re


def _report_file_name(company_name):
        safe_name = re.sub(r"[^a-zA-Z0-9]+", "-", company_name.strip().lower()).strip("-")
        return f"report-{safe_name or 'report'}.html"


def _extract_text(content):
        if isinstance(content, str):
                return content

        if isinstance(content, list):
                text_parts = []
                for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                                text_parts.append(block.get("text", ""))
                if text_parts:
                        return "\n\n".join(part for part in text_parts if part)

        return str(content)


def _markdownish_to_html(text):
        lines = text.splitlines()
        html_parts = []
        in_list = False

        def _inline_markup(value):
                escaped = escape(value)
                escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
                escaped = re.sub(r"__(.+?)__", r"<strong>\1</strong>", escaped)
                return escaped

        for raw_line in lines:
                line = raw_line.strip()

                if not line:
                        if in_list:
                                html_parts.append("</ul>")
                                in_list = False
                        continue

                if line.startswith("# "):
                        if in_list:
                                html_parts.append("</ul>")
                                in_list = False
                        html_parts.append(f"<h1>{_inline_markup(line[2:].strip())}</h1>")
                        continue

                if line.startswith("## "):
                        if in_list:
                                html_parts.append("</ul>")
                                in_list = False
                        html_parts.append(f"<h2>{_inline_markup(line[3:].strip())}</h2>")
                        continue

                if line.startswith("- ") or line.startswith("* "):
                        if not in_list:
                                html_parts.append("<ul>")
                                in_list = True
                        html_parts.append(f"<li>{_inline_markup(line[2:].strip())}</li>")
                        continue

                if in_list:
                        html_parts.append("</ul>")
                        in_list = False

                html_parts.append(f"<p>{_inline_markup(line)}</p>")

        if in_list:
                html_parts.append("</ul>")

        return "\n".join(html_parts)


def _render_report_html(report_text):
        from pathlib import Path
        content_html = _markdownish_to_html(report_text)
        template_path = Path(__file__).parent / "template.html"
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        return template.replace("<!-- Report content will be inserted here -->", content_html)

def run():
        agent = create_agent()

        company = input("Enter company name: ")

        result = agent.invoke({
                "messages": [("user", company)]
        })

        final_answer = result["messages"][-1].content
        report_text = _extract_text(final_answer)
        print("\n\n", report_text)

        html_report = _render_report_html(report_text)
        report_file_name = _report_file_name(company)
        with open(report_file_name, "w", encoding="utf-8") as f:
                f.write(html_report)

        print(f"\nSaved HTML report to: {report_file_name}")


if __name__ == "__main__":
    run()