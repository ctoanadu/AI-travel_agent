# 🧳 Travel Agent Chatbot

An intelligent travel assistant built using **LangGraph**, **LangChain**, **SerpAPI**, **OpenAI GPT-4o**, and **Streamlit**.

This chatbot helps users find **real-time flights and hotels** using natural language, powered by tool-assisted reasoning via GPT-4o and SerpAPI.

---

## ✨ Features

- 🔍 Real-time search for flights and hotels
- 🤖 Uses GPT-4o to reason and decide when to call external tools
- 🛠️ Tools connected via LangGraph flow control
- 💬 Clean frontend UI built with Streamlit
- 🔐 API key management with dotenv

---

## 🧱 Tech Stack

| Feature            | Technology             |
|--------------------|-------------------------|
| LLM                | OpenAI GPT-4o           |
| Tool Orchestration | LangGraph + LangChain   |
| APIs               | SerpAPI (Google Hotels & Flights) |
| UI                 | Streamlit               |
| Environment Vars   | Python Dotenv           |

---

## 📁 Project Structure

```
travel-agent-chatbot/
│
├── agents/
│   ├── agent.py                 # LangGraph-based smart agent
│   └── tools/
│       ├── flights_searcher.py  # Tool for searching flights
│       └── hotels_searcher.py   # Tool for searching hotels
│
├── app.py                       # Streamlit-based frontend
├── .env                         # API keys file (excluded from Git)
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/travel-agent-chatbot.git
cd travel-agent-chatbot
```

### 2. Set Up Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Setup

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
SERPAPI_API_KEY=your_serpapi_api_key_here
```

> ✅ Make sure your `.env` file is listed in `.gitignore` to keep API keys safe.

---

## ▶️ Running the App

Launch the Streamlit app with:

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 💬 Example Prompts

Try asking the chatbot:

- "Find me a flight from New York to London from July 5th to July 15th"
- "I need a hotel in Paris for 3 nights starting August 10th"
- "Show me multi-city flights from LA to Tokyo to Bangkok in September"

---

## 🧪 Features in Action

### 🔧 Tool-Based Reasoning

When GPT-4o receives a query, it decides whether to use the `flights_searcher` or `hotels_searcher` tool, fetches data using SerpAPI, and responds accordingly.

---

## 🖼️ Screenshots

> 📸 UI showing user and assistant interaction  
![Interface Preview](images/interface-preview.png)

> 📸 Results with hotel listings and flight data  
![Search Results](images/results-sample.png)

---

## 🧾 Requirements

Make sure the following are in `requirements.txt`:

```
openai
langchain
langgraph
streamlit
python-dotenv
serpapi
```

---

## 📌 Notes

- GPT-4o API usage may incur costs depending on your OpenAI plan.
- SerpAPI offers a free tier with limited searches — you may need a paid key for higher volume.

---

## 🤝 Contributing

Feel free to open issues or submit pull requests to improve this project!

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
