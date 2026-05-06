# 📊 Market Researcher AI

An advanced agentic research tool that gathers live web data, performs sentiment analysis, and generates structured, high-end Investment Memos.

## ✨ Features

- **Agentic Research**: Powered by LangGraph for multi-step reasoning and search.
- **Live Web Access**: Real-time searching via DuckDuckGo and deep scraping with BeautifulSoup.
- **Sentiment Analysis**: Automated bullish and bearish perspective generation.
- **Antigravity UI**: Premium glassmorphism-based HTML reports with smooth GSAP animations and 3D depth.
- **Dual Interface**: Choose between a high-density Streamlit Web UI or a lean CLI.
- **Export Ready**: Download beautiful, self-contained HTML reports for stakeholders.

## 🛠️ Tech Stack

- **Framework**: LangChain & LangGraph
- **Intelligence**: Z.ai GLM-4.6 (OpenAI-compatible)
- **Interface**: Streamlit
- **Animations**: GSAP (GreenSock)
- **Styling**: CSS Glassmorphism & Custom 3D Transforms

## 🚀 Getting Started

Follow these steps to set up the project on your local machine.

### 1. Clone the Repository

```powershell
git clone https://github.com/HadiuzzamanBappy/Research-Tool.git
cd Research-Tool
```

### 2. Create and Activate Virtual Environment

**Windows:**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configuration

Create a `.env` file in the root directory (you can copy `.env.local` if it exists):

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.z.ai/v1  # If using Z.ai
```

## 🎮 How to Run

### Web Dashboard (Recommended)

This provides a real-time "Thinking Stream" and interactive report preview.

```powershell
streamlit run app.py
```

### Command Line Interface

For quick, terminal-based research.

```powershell
python main.py
```

## 📄 Output & Exports

The tool generates **"Investment Memos"** designed with the **Antigravity Design System**. These reports feature:

- **Glassmorphism**: Sophisticated translucent surfaces.
- **Motion Design**: Staggered entrance animations for content.
- **Interactive Depth**: 3D tilt effects on mouse hover.
- **Self-Contained**: All styles and scripts are embedded in a single HTML file for easy sharing.

---
Developed by [Hadiuzzaman Bappy](https://github.com/HadiuzzamanBappy)
