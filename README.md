# Market Researcher

An AI market research agent that gathers live web data and generates a structured investment memo for a company.

## Features

- Web search using DuckDuckGo
- Website scraping with BeautifulSoup
- Bullish and bearish sentiment analysis
- Streamed thinking and final result in the web UI
- Markdown-to-HTML export for the final report

## Tech Stack

- LangChain
- LangGraph
- Z.ai GLM-4.6 via the OpenAI-compatible client
- Streamlit
- Python

## Setup

```powershell
git clone https://github.com/HadiuzzamanBappy/Research-Tool.git
cd Research-Tool
python -m pip install -r requirements.txt
set ZAI_API_KEY=your_z_ai_api_key_here
```

## Run the CLI

```powershell
python main.py
```

## Run the Web UI

```powershell
streamlit run app.py
```

The app will open in your browser, usually at `http://localhost:8501`.

## Output

- The web UI shows the thinking stream separately from the final memo.
- The final memo can be downloaded as HTML using the built-in export.
- The HTML export uses proper Markdown rendering, including bold text, headings, and lists.
