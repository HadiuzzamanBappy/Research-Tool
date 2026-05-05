import re
import time
import streamlit as st

from agent.agent import create_agent
from main import _extract_text, _render_report_html


st.set_page_config(page_title="Market Researcher", page_icon="📊", layout="wide")

st.title("Market Researcher Web UI")
st.caption("Generate an investment memo for a company using Z.ai GLM-5 + web research tools.")

company = st.text_input("Company name", placeholder="e.g. Microsoft")
run = st.button("Run Research", type="primary")

if "thinking_text" not in st.session_state:
    st.session_state.thinking_text = ""

if "result_text" not in st.session_state:
    st.session_state.result_text = ""

if "report_html" not in st.session_state:
    st.session_state.report_html = ""


def _stream_with_split(agent, prompt: str):
    """
    Stream everything from AI in real-time.
    Yields tuples: (chunk_text, is_final)
    is_final=True when we've crossed the report start marker.
    """
    final_marker = re.compile(r'(#\s*Investment Memo\b|##\s*1\.?\s*Company Overview\b)', re.I)
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

        # Normalize invisible characters only
        chunk_text = chunk_text.replace("\u200b", "").replace("\ufeff", "")
        
        previous_length = len(full_response)
        full_response += chunk_text

        # Detect the first complete report marker across the full accumulated stream.
        if not seen_marker:
            match = final_marker.search(full_response)
            if match:
                seen_marker = True
                split_index = match.start()

                # Emit any newly arrived thinking text before the marker.
                if split_index > previous_length:
                    thinking_part = full_response[previous_length:split_index]
                    if thinking_part:
                        yield thinking_part, False

                # Emit the result starting exactly at the memo heading.
                result_part = full_response[split_index:]
                if result_part:
                    yield result_part, True
                continue

        # Stream everything - thinking until the marker is found, then result.
        yield chunk_text, seen_marker


def _typewriter(text: str):
    """Yield text one character at a time for a chat-like typing effect."""
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

            agent = create_agent()

            st.info("🔍 Researching...")

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
                                with st.expander("🧠 Thinking Process", expanded=thinking_is_open):
                                    st.text(thinking_text)
                    else:
                        if thinking_is_open:
                            thinking_is_open = False
                            with thinking_expander_container.container():
                                with st.expander("🧠 Thinking Process", expanded=False):
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
                        file_name="report.html",
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
        with st.expander("🧠 Thinking Process", expanded=False):
            st.text(st.session_state.thinking_text)

    if st.session_state.result_text:
        st.markdown(st.session_state.result_text)

    if st.session_state.report_html:
        st.download_button(
            label="📥 Download HTML report",
            data=st.session_state.report_html,
            file_name="report.html",
            mime="text/html",
        )