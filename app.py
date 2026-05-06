import re
import time
import streamlit as st

from agent.agent import create_agent
from agent.prompt import detect_input_type
from main import _extract_text, _render_report_html


st.set_page_config(page_title="Market Researcher", page_icon="📊", layout="wide")

st.title("Research tool")
st.caption("Research companies, topics, URLs, and general inputs with live web research tools.")

# Single row layout
col_type, col_input, col_lang, col_run = st.columns([1.2, 5, 1.2, 1.3])

with col_type:
    selection = st.selectbox(
        "Input type",
        options=["Auto", "Company", "URL", "Topic", "How to"],
        index=0,
        help="Choose how to interpret the input. 'Auto' will detect type automatically.",
        label_visibility="collapsed"
    )

with col_input:
    if selection == "Auto":
        placeholder = "e.g. Microsoft, https://example.com/article, a short topic, or a product"
    elif selection == "Company":
        placeholder = "e.g. Microsoft Corporation, Tesla, Amazon"
    elif selection == "URL":
        placeholder = "e.g. https://example.com/article-or-page"
    elif selection == "Topic":
        placeholder = "e.g. electric vehicles, market sizing, fintech trends"
    elif selection == "How to":
        placeholder = "e.g. how to cook rice, how to create a battery"
    else:
        placeholder = "Enter what you want researched"

    company = st.text_input("What should the agent research?", placeholder=placeholder, label_visibility="collapsed")

with col_lang:
    language = st.selectbox(
        "Language",
        options=["English", "Bengali"],
        index=0,
        help="The language of the final research report.",
        label_visibility="collapsed"
    )

with col_run:
    st.markdown(
        """
        <style>
        div.stVerticalBlock {
            display: flex;
            justify-content: flex-end;
            width: 100%;
        }
        div.stButton > button {
            box-shadow: 0 0 10px rgba(0,150,255,0.45);
            transition: box-shadow 0.18s ease-in-out, transform 0.08s;
            width: 100%;
            height: 38px;
        }
        div.stButton > button:hover {
            box-shadow: 0 0 22px rgba(0,150,255,0.75);
            transform: translateY(-1px);
        }
        /* Align inputs vertically */
        .stSelectbox, .stTextInput {
            margin-bottom: 0px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    run = st.button("Run Research", type="primary")

if "thinking_text" not in st.session_state:
    st.session_state.thinking_text = ""

if "result_text" not in st.session_state:
    st.session_state.result_text = ""

if "report_html" not in st.session_state:
    st.session_state.report_html = ""


def _report_file_name(company_name: str) -> str:
    safe_name = re.sub(r"[^a-zA-Z0-9]+", "-", company_name.strip().lower()).strip("-")
    return f"report-{safe_name or 'report'}.html"


def _stream_with_split(agent, prompt: str):
    """
    Stream everything from AI in real-time.
    Yields tuples: (chunk_text, is_final)
    is_final=True when we've crossed the report start marker.
    """
    final_marker = re.compile(r"#{1,3}\s+", re.I)
    seen_marker = False
    full_response = ""

    for event in agent.stream({"messages": [("user", prompt)]}, stream_mode="messages"):
        chunk = event[0] if isinstance(event, tuple) else event
        chunk_text = getattr(chunk, "content", "")

        if not chunk_text:
            continue

        if isinstance(chunk_text, list):
            chunk_text = _extract_text(chunk_text)

        if not chunk_text:
            continue

        chunk_text = chunk_text.replace("\u200b", "").replace("\ufeff", "")

        previous_length = len(full_response)
        full_response += chunk_text

        if not seen_marker:
            match = final_marker.search(full_response)
            if match:
                seen_marker = True
                split_index = match.start()

                if split_index > previous_length:
                    thinking_part = full_response[previous_length:split_index]
                    if thinking_part:
                        yield thinking_part, False

                result_part = full_response[split_index:]
                if result_part:
                    yield result_part, True
                continue

        yield chunk_text, seen_marker


def _typewriter(text: str):
    for character in text:
        yield character
        time.sleep(0.002)


if run:
    if not company.strip():
        st.warning("Please enter a company name.")
    else:
        try:
            st.session_state.thinking_text = ""
            st.session_state.result_text = ""
            st.session_state.report_html = ""

            profile = selection.lower() if selection != "Auto" else detect_input_type(company)
            if profile == "how to":
                profile = "howto"
            agent = create_agent(company, profile, language)

            st.info(f"🔍 Researching ({profile})...")

            try:
                thinking_text = ""
                result_text = ""
                thinking_expander_container = st.empty()
                result_container = st.empty()
                thinking_is_open = True

                for chunk, is_final in _stream_with_split(agent, company.strip()):
                    if not is_final:
                        for character in _typewriter(chunk):
                            thinking_text += character
                            st.session_state.thinking_text = thinking_text
                            with thinking_expander_container.container():
                                with st.expander("🧠 Researching", expanded=thinking_is_open):
                                    st.text(thinking_text)
                    else:
                        if thinking_is_open:
                            thinking_is_open = False
                            with thinking_expander_container.container():
                                with st.expander("🧠 Researching", expanded=False):
                                    st.text(thinking_text)

                        for character in _typewriter(chunk):
                            result_text += character
                            st.session_state.result_text = result_text
                            result_container.markdown(result_text)

                if result_text:
                    st.success("✅ Research complete")
                    st.session_state.thinking_text = thinking_text
                    st.session_state.result_text = result_text
                    st.session_state.report_html = _render_report_html(result_text)
                    st.download_button(
                        label="📥 Download HTML report",
                        data=st.session_state.report_html,
                        file_name=_report_file_name(company),
                        mime="text/html",
                    )
                elif thinking_text:
                    st.success("✅ Research complete")
                    st.session_state.thinking_text = thinking_text

            except Exception as stream_err:
                st.error(f"Streaming error: {stream_err}")
                st.info("Tip: Check if your Z.ai account has sufficient balance/quota. Visit z.ai/manage-apikey/billing")
                st.stop()

        except Exception as exc:
            st.error(f"Failed to run research: {exc}")

if not run and (st.session_state.thinking_text or st.session_state.result_text):
    if st.session_state.thinking_text:
        with st.expander("🧠 Researching", expanded=False):
            st.text(st.session_state.thinking_text)

    if st.session_state.result_text:
        st.markdown(st.session_state.result_text)

    if st.session_state.report_html:
        st.download_button(
            label="📥 Download HTML report",
            data=st.session_state.report_html,
            file_name=_report_file_name(company) if company.strip() else "report.html",
            mime="text/html",
        )
